import { writable } from 'svelte/store';

export interface ToastMessage {
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    duration: number;
}

function createToastStore() {
    const { subscribe, update } = writable<ToastMessage[]>([]);

    function add(type: ToastMessage['type'], message: string, duration = 5000) {
        const id = crypto.randomUUID();
        const toast: ToastMessage = { id, type, message, duration };
        
        update(toasts => [...toasts, toast]);

        if (duration > 0) {
            setTimeout(() => dismiss(id), duration);
        }

        return id;
    }

    function dismiss(id: string) {
        update(toasts => toasts.filter(t => t.id !== id));
    }

    return {
        subscribe,
        success: (message: string, duration = 5000) => add('success', message, duration),
        error: (message: string, duration = 7000) => add('error', message, duration),
        warning: (message: string, duration = 5000) => add('warning', message, duration),
        info: (message: string, duration = 5000) => add('info', message, duration),
        dismiss
    };
}

export const toasts = createToastStore();
