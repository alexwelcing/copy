from service.api.schemas import SkillName, WorkRequest

def test_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "skills_available" in data

def test_list_skills(api_client):
    response = api_client.get("/skills")
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert "copywriting" in data["skills"]["writing"]

def test_skill_execution_mock_structure(executor):
    """
    Verify that the executor can load a skill and build a prompt.
    Does NOT call the live LLM API to save costs/time.
    """
    request = WorkRequest(
        skill=SkillName.COPYWRITING,
        task="Write a headline",
        context={"product": "TestWidget"}
    )
    
    prompt = executor.build_prompt(request)
    assert "## Skill Framework" in prompt
    assert "Write a headline" in prompt
    assert "**product**: TestWidget" in prompt

# Note: Integration tests calling real LLMs should be marked or separate
