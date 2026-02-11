/**
 * HIGH ERA AGENCY - Cloudflare Sprite Runtime
 *
 * Sprites as Durable Objects - stateful AI agents at the edge.
 *
 * Each sprite is a Durable Object instance with:
 * - Persistent state (current task, conversation history)
 * - WebSocket connections for real-time updates
 * - Outbound HTTP (Claude API, Fal API, etc.)
 * - Automatic hibernation when idle
 */

import { DurableObject } from "cloudflare:workers";
import { CompetitiveAnalyst } from "./analyst";

// Re-export for wrangler
export { CompetitiveAnalyst };

// Types
export interface Env {
  SPRITES: DurableObjectNamespace<Sprite>;
  SWARM: DurableObjectNamespace<SwarmCoordinator>;
  ANALYST: DurableObjectNamespace<CompetitiveAnalyst>;
  ASSETS: R2Bucket;
  DB: D1Database;
  ANTHROPIC_API_KEY: string;
  FAL_API_KEY: string;
  // Optional research API keys
  AHREFS_API_KEY?: string;
  SEMRUSH_API_KEY?: string;
  SIMILARWEB_API_KEY?: string;
  BUILTWITH_API_KEY?: string;
}

export interface SpriteConfig {
  tenantId: string;
  agentType: AgentType;
  projectId?: string;
  brandContext?: BrandContext;
}

export interface BrandContext {
  voice: string;
  tone: string;
  audience: string;
  guidelines: string[];
}

export type AgentType =
  | "director"
  | "strategist"
  | "copywriter"
  | "editor"
  | "optimizer"
  | "analyst";

export type SpriteStatus = "starting" | "idle" | "working" | "stopped";

interface Task {
  id: string;
  description: string;
  context?: Record<string, unknown>;
  submittedAt: number;
}

interface ExecutionResult {
  output: string;
  tokensUsed: number;
  handoffRequested?: { targetAgent: AgentType; context: string };
  reviewRequested?: { content: string };
}

// Agent personas (loaded from KV or embedded)
const AGENT_PERSONAS: Record<AgentType, string> = {
  director: `You are the Director - the orchestrator of the agency.
You coordinate projects, assign work to specialists, and ensure delivery.
When you need specialized work, hand off to the appropriate agent.`,

  strategist: `You are the Strategist - the strategic mind of the agency.
You handle positioning, psychology, competitive analysis, and go-to-market strategy.
You think before you write. Strategy precedes execution.`,

  copywriter: `You are the Copywriter - the voice of the agency.
You write headlines, landing pages, emails, ads, and all customer-facing copy.
Every word earns its place. Clarity over cleverness.`,

  editor: `You are the Editor - the quality gate of the agency.
You polish, refine, and ensure consistency across all copy.
You catch what others miss. Standards without ego.`,

  optimizer: `You are the Optimizer - the conversion specialist.
You handle CRO, page structure, funnel analysis, and growth experiments.
Data informs intuition. Test everything.`,

  analyst: `You are the Analyst - the measurement expert.
You handle tracking, attribution, dashboards, and insights.
Numbers tell stories. Find the signal in the noise.`,
};

/**
 * Sprite Durable Object
 *
 * A single AI agent instance. Handles:
 * - Task execution via Claude API
 * - State persistence
 * - WebSocket connections for real-time updates
 * - Handoffs to other sprites
 */
export class Sprite extends DurableObject<Env> {
  private config: SpriteConfig | null = null;
  private status: SpriteStatus = "starting";
  private currentTask: Task | null = null;
  private tokensUsed = 0;
  private tasksCompleted = 0;
  private conversationHistory: Array<{ role: string; content: string }> = [];
  private connections: Set<WebSocket> = new Set();

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
  }

  /**
   * Initialize sprite with configuration
   */
  async initialize(config: SpriteConfig): Promise<void> {
    this.config = config;
    this.status = "idle";

    // Persist config
    await this.ctx.storage.put("config", config);
    await this.ctx.storage.put("status", this.status);

    // Set alarm for idle timeout (5 minutes)
    await this.ctx.storage.setAlarm(Date.now() + 5 * 60 * 1000);

    this.broadcast({ type: "initialized", agentType: config.agentType });
  }

  /**
   * Submit work to this sprite
   */
  async submitWork(task: Task): Promise<ExecutionResult> {
    if (!this.config) {
      throw new Error("Sprite not initialized");
    }

    this.status = "working";
    this.currentTask = task;
    await this.ctx.storage.put("status", this.status);
    await this.ctx.storage.put("currentTask", task);

    this.broadcast({ type: "working", taskId: task.id });

    try {
      const result = await this.execute(task);

      this.tasksCompleted++;
      this.tokensUsed += result.tokensUsed;
      this.currentTask = null;
      this.status = "idle";

      await this.ctx.storage.put("status", this.status);
      await this.ctx.storage.put("tokensUsed", this.tokensUsed);
      await this.ctx.storage.put("tasksCompleted", this.tasksCompleted);
      await this.ctx.storage.delete("currentTask");

      // Reset idle timeout
      await this.ctx.storage.setAlarm(Date.now() + 5 * 60 * 1000);

      this.broadcast({
        type: "complete",
        taskId: task.id,
        output: result.output,
      });

      return result;
    } catch (error) {
      this.status = "idle";
      this.currentTask = null;
      await this.ctx.storage.put("status", this.status);

      this.broadcast({
        type: "error",
        taskId: task.id,
        error: String(error),
      });

      throw error;
    }
  }

  /**
   * Execute task via Claude API
   */
  private async execute(task: Task): Promise<ExecutionResult> {
    const persona = AGENT_PERSONAS[this.config!.agentType];
    const brandContext = this.config!.brandContext;

    // Build system prompt
    let systemPrompt = persona;
    if (brandContext) {
      systemPrompt += `\n\nBrand Context:
Voice: ${brandContext.voice}
Tone: ${brandContext.tone}
Audience: ${brandContext.audience}
Guidelines: ${brandContext.guidelines.join(", ")}`;
    }

    // Add conversation history
    const messages = [
      ...this.conversationHistory,
      { role: "user", content: task.description },
    ];

    // Call Claude API
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        system: systemPrompt,
        messages: messages.map((m) => ({
          role: m.role as "user" | "assistant",
          content: m.content,
        })),
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Claude API error: ${response.status} - ${error}`);
    }

    const data = (await response.json()) as {
      content: Array<{ type: string; text: string }>;
      usage: { input_tokens: number; output_tokens: number };
    };

    const output = data.content
      .filter((c) => c.type === "text")
      .map((c) => c.text)
      .join("\n");

    const tokensUsed = data.usage.input_tokens + data.usage.output_tokens;

    // Update conversation history
    this.conversationHistory.push(
      { role: "user", content: task.description },
      { role: "assistant", content: output }
    );

    // Keep history manageable (last 10 exchanges)
    if (this.conversationHistory.length > 20) {
      this.conversationHistory = this.conversationHistory.slice(-20);
    }

    await this.ctx.storage.put("conversationHistory", this.conversationHistory);

    // Parse for handoff/review requests
    const handoffMatch = output.match(
      /\[HANDOFF:(\w+)\]([\s\S]*?)\[\/HANDOFF\]/
    );
    const reviewMatch = output.match(/\[REVIEW\]([\s\S]*?)\[\/REVIEW\]/);

    return {
      output,
      tokensUsed,
      handoffRequested: handoffMatch
        ? {
            targetAgent: handoffMatch[1] as AgentType,
            context: handoffMatch[2].trim(),
          }
        : undefined,
      reviewRequested: reviewMatch
        ? { content: reviewMatch[1].trim() }
        : undefined,
    };
  }

  /**
   * Generate image via Fal API
   */
  async generateImage(
    prompt: string,
    outputPath: string
  ): Promise<{ url: string; r2Path: string }> {
    // Call Fal API
    const response = await fetch("https://fal.run/fal-ai/flux-pro/v1.1", {
      method: "POST",
      headers: {
        Authorization: `Key ${this.env.FAL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt,
        image_size: { width: 1920, height: 1080 },
        num_images: 1,
      }),
    });

    if (!response.ok) {
      throw new Error(`Fal API error: ${response.status}`);
    }

    const data = (await response.json()) as {
      images: Array<{ url: string }>;
    };

    const imageUrl = data.images[0]?.url;
    if (!imageUrl) {
      throw new Error("No image returned from Fal");
    }

    // Download and store in R2
    const imageResponse = await fetch(imageUrl);
    const imageData = await imageResponse.arrayBuffer();

    const r2Path = `${this.config!.tenantId}/${outputPath}`;
    await this.env.ASSETS.put(r2Path, imageData, {
      httpMetadata: { contentType: "image/png" },
    });

    return {
      url: imageUrl,
      r2Path,
    };
  }

  /**
   * Handle WebSocket connections for real-time updates
   */
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // WebSocket upgrade
    if (request.headers.get("Upgrade") === "websocket") {
      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);

      this.ctx.acceptWebSocket(server);
      this.connections.add(server);

      // Send current state
      server.send(
        JSON.stringify({
          type: "state",
          status: this.status,
          agentType: this.config?.agentType,
          currentTask: this.currentTask,
          tokensUsed: this.tokensUsed,
          tasksCompleted: this.tasksCompleted,
        })
      );

      return new Response(null, { status: 101, webSocket: client });
    }

    // REST API
    if (url.pathname === "/status") {
      return Response.json({
        status: this.status,
        agentType: this.config?.agentType,
        tenantId: this.config?.tenantId,
        currentTask: this.currentTask,
        tokensUsed: this.tokensUsed,
        tasksCompleted: this.tasksCompleted,
      });
    }

    if (url.pathname === "/work" && request.method === "POST") {
      const task = (await request.json()) as Task;
      const result = await this.submitWork(task);
      return Response.json(result);
    }

    if (url.pathname === "/generate-image" && request.method === "POST") {
      const { prompt, outputPath } = (await request.json()) as {
        prompt: string;
        outputPath: string;
      };
      const result = await this.generateImage(prompt, outputPath);
      return Response.json(result);
    }

    return new Response("Not found", { status: 404 });
  }

  /**
   * Handle WebSocket messages
   */
  async webSocketMessage(ws: WebSocket, message: string): Promise<void> {
    const data = JSON.parse(message);

    if (data.type === "ping") {
      ws.send(JSON.stringify({ type: "pong" }));
    }
  }

  /**
   * Handle WebSocket close
   */
  async webSocketClose(ws: WebSocket): Promise<void> {
    this.connections.delete(ws);
  }

  /**
   * Broadcast to all connected WebSockets
   */
  private broadcast(message: Record<string, unknown>): void {
    const json = JSON.stringify(message);
    for (const ws of this.connections) {
      try {
        ws.send(json);
      } catch {
        this.connections.delete(ws);
      }
    }
  }

  /**
   * Alarm handler - idle timeout
   */
  async alarm(): Promise<void> {
    if (this.status === "idle" && !this.currentTask) {
      this.status = "stopped";
      await this.ctx.storage.put("status", this.status);
      this.broadcast({ type: "stopped", reason: "idle_timeout" });

      // Close all connections
      for (const ws of this.connections) {
        ws.close(1000, "Sprite stopped due to idle timeout");
      }
      this.connections.clear();
    }
  }

  /**
   * Restore state on wake from hibernation
   */
  async restoreState(): Promise<void> {
    this.config = await this.ctx.storage.get("config");
    this.status = (await this.ctx.storage.get("status")) || "starting";
    this.tokensUsed = (await this.ctx.storage.get("tokensUsed")) || 0;
    this.tasksCompleted = (await this.ctx.storage.get("tasksCompleted")) || 0;
    this.conversationHistory =
      (await this.ctx.storage.get("conversationHistory")) || [];
    this.currentTask = await this.ctx.storage.get("currentTask");
  }
}

/**
 * Swarm Coordinator Durable Object
 *
 * Manages all sprites for a tenant. Handles:
 * - Sprite lifecycle (spawn, stop)
 * - Work routing
 * - Handoffs between sprites
 * - Usage tracking
 */
export class SwarmCoordinator extends DurableObject<Env> {
  private tenantId: string | null = null;
  private sprites: Map<string, { agentType: AgentType; status: SpriteStatus }> =
    new Map();

  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // Initialize coordinator for tenant
    if (url.pathname === "/init" && request.method === "POST") {
      const { tenantId } = (await request.json()) as { tenantId: string };
      this.tenantId = tenantId;
      await this.ctx.storage.put("tenantId", tenantId);
      return Response.json({ ok: true });
    }

    // Spawn a new sprite
    if (url.pathname === "/spawn" && request.method === "POST") {
      const config = (await request.json()) as SpriteConfig;
      const spriteId = crypto.randomUUID();

      // Get sprite DO
      const spriteStub = this.env.SPRITES.get(
        this.env.SPRITES.idFromName(`${this.tenantId}:${spriteId}`)
      );

      // Initialize it
      await spriteStub.initialize(config);

      this.sprites.set(spriteId, {
        agentType: config.agentType,
        status: "idle",
      });
      await this.ctx.storage.put("sprites", Object.fromEntries(this.sprites));

      return Response.json({ spriteId });
    }

    // List sprites
    if (url.pathname === "/sprites" && request.method === "GET") {
      return Response.json(Object.fromEntries(this.sprites));
    }

    // Submit work (auto-routes to appropriate sprite)
    if (url.pathname === "/work" && request.method === "POST") {
      const { task, agentType } = (await request.json()) as {
        task: Task;
        agentType?: AgentType;
      };

      // Find or spawn appropriate sprite
      const targetType = agentType || this.inferAgentType(task.description);
      let spriteId = this.findSpriteByType(targetType);

      if (!spriteId) {
        // Spawn new sprite
        const config: SpriteConfig = {
          tenantId: this.tenantId!,
          agentType: targetType,
        };

        spriteId = crypto.randomUUID();
        const spriteStub = this.env.SPRITES.get(
          this.env.SPRITES.idFromName(`${this.tenantId}:${spriteId}`)
        );
        await spriteStub.initialize(config);

        this.sprites.set(spriteId, { agentType: targetType, status: "idle" });
      }

      // Submit work
      const spriteStub = this.env.SPRITES.get(
        this.env.SPRITES.idFromName(`${this.tenantId}:${spriteId}`)
      );

      const result = await spriteStub.submitWork(task);
      return Response.json({ spriteId, result });
    }

    return new Response("Not found", { status: 404 });
  }

  private inferAgentType(description: string): AgentType {
    const lower = description.toLowerCase();

    if (
      lower.includes("strategy") ||
      lower.includes("position") ||
      lower.includes("competitor")
    ) {
      return "strategist";
    }
    if (
      lower.includes("write") ||
      lower.includes("copy") ||
      lower.includes("headline")
    ) {
      return "copywriter";
    }
    if (
      lower.includes("edit") ||
      lower.includes("review") ||
      lower.includes("polish")
    ) {
      return "editor";
    }
    if (
      lower.includes("convert") ||
      lower.includes("optimize") ||
      lower.includes("cro")
    ) {
      return "optimizer";
    }
    if (
      lower.includes("track") ||
      lower.includes("measure") ||
      lower.includes("analytics")
    ) {
      return "analyst";
    }

    return "director";
  }

  private findSpriteByType(agentType: AgentType): string | null {
    for (const [id, info] of this.sprites) {
      if (info.agentType === agentType && info.status === "idle") {
        return id;
      }
    }
    return null;
  }
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === "/health") {
      return new Response("ok");
    }

    // Route to coordinator for tenant operations
    if (url.pathname.startsWith("/tenant/")) {
      const tenantId = url.pathname.split("/")[2];
      const coordinatorId = env.SWARM.idFromName(tenantId);
      const coordinator = env.SWARM.get(coordinatorId);

      // Forward request with modified path
      const newUrl = new URL(request.url);
      newUrl.pathname = url.pathname.replace(`/tenant/${tenantId}`, "");

      return coordinator.fetch(new Request(newUrl.toString(), request));
    }

    // Route to specific sprite
    if (url.pathname.startsWith("/sprite/")) {
      const parts = url.pathname.split("/");
      const tenantId = parts[2];
      const spriteId = parts[3];

      const sprite = env.SPRITES.get(
        env.SPRITES.idFromName(`${tenantId}:${spriteId}`)
      );

      const newUrl = new URL(request.url);
      newUrl.pathname = "/" + parts.slice(4).join("/");

      return sprite.fetch(new Request(newUrl.toString(), request));
    }

    // Route to competitive analyst
    // /analyst/{tenant}/research - full competitive research
    // /analyst/{tenant}/scan - quick competitor scan
    // /analyst/{tenant}/find-competitors - discover competitors
    // /analyst/{tenant}/seo-gap - SEO gap analysis
    if (url.pathname.startsWith("/analyst/")) {
      const parts = url.pathname.split("/");
      const tenantId = parts[2];

      const analyst = env.ANALYST.get(
        env.ANALYST.idFromName(`analyst:${tenantId}`)
      );

      const newUrl = new URL(request.url);
      newUrl.pathname = "/" + parts.slice(3).join("/");

      return analyst.fetch(new Request(newUrl.toString(), request));
    }

    return new Response("High Era Agency - Sprite Runtime", {
      headers: { "Content-Type": "text/plain" },
    });
  },
};
