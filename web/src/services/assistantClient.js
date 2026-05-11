const ASSISTANT_API_BASE_URL_FALLBACK = "http://127.0.0.1:8000";
const ASSISTANT_SESSION_STORAGE_KEY =
    "always-beautiful:assistant-session-id";
const ASSISTANT_ALLOWED_CHANNELS = new Set(["web", "whatsapp", "admin"]);

export const ASSISTANT_CHANNEL_WEB = "web";

export class AssistantClientError extends Error {
    constructor(message, options = {}) {
        super(message);
        this.name = "AssistantClientError";
        this.status = options.status ?? null;
        this.payload = options.payload ?? null;
    }
}

export function getAssistantApiBaseUrl() {
    const configuredBaseUrl =
        import.meta.env?.VITE_ASSISTANT_API_BASE_URL?.trim();

    return configuredBaseUrl || ASSISTANT_API_BASE_URL_FALLBACK;
}

function buildAssistantApiUrl(path) {
    const baseUrl = getAssistantApiBaseUrl().replace(/\/+$/, "");
    const normalizedPath = path.startsWith("/") ? path : `/${path}`;

    return `${baseUrl}${normalizedPath}`;
}

function assertNonBlankString(value, fieldName) {
    if (typeof value !== "string" || !value.trim()) {
        throw new AssistantClientError(`${fieldName} must be a non-empty string.`);
    }

    return value.trim();
}

function parseAssistantResponsePayload(payload) {
    return {
        sessionId: payload?.session_id,
        intent: payload?.intent,
        message: payload?.message,
        requiresDeposit: Boolean(payload?.requires_deposit),
        depositPercentage: Number(payload?.deposit_percentage ?? 0),
        nextActions: Array.isArray(payload?.next_actions)
            ? payload.next_actions
            : [],
        raw: payload,
    };
}

async function parseJsonSafely(response) {
    const responseText = await response.text();

    if (!responseText) {
        return null;
    }

    try {
        return JSON.parse(responseText);
    } catch {
        return null;
    }
}

function createAssistantSessionId() {
    if (globalThis.crypto?.randomUUID) {
        return `web-assistant-${globalThis.crypto.randomUUID()}`;
    }

    const timestamp = Date.now().toString(36);
    const randomValue = Math.random().toString(36).slice(2, 12);

    return `web-assistant-${timestamp}-${randomValue}`;
}

export function getOrCreateAssistantSessionId() {
    const storage = globalThis.localStorage;

    if (!storage) {
        return createAssistantSessionId();
    }

    const storedSessionId = storage.getItem(ASSISTANT_SESSION_STORAGE_KEY);

    if (storedSessionId?.trim()) {
        return storedSessionId;
    }

    const sessionId = createAssistantSessionId();
    storage.setItem(ASSISTANT_SESSION_STORAGE_KEY, sessionId);

    return sessionId;
}

export async function sendAssistantMessage({
    sessionId,
    message,
    channel = ASSISTANT_CHANNEL_WEB,
}) {
    const validatedSessionId = assertNonBlankString(sessionId, "sessionId");
    const trimmedMessage = assertNonBlankString(message, "message");
    const validatedChannel = assertNonBlankString(channel, "channel");

    if (!ASSISTANT_ALLOWED_CHANNELS.has(validatedChannel)) {
        throw new AssistantClientError(
            "channel must be one of: web, whatsapp, admin."
        );
    }

    const response = await fetch(buildAssistantApiUrl("/assistant/chat"), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            session_id: validatedSessionId,
            message: trimmedMessage,
            channel: validatedChannel,
        }),
    });
    const payload = await parseJsonSafely(response);

    if (!response.ok) {
        throw new AssistantClientError(
            `Assistant request failed with status ${response.status}.`,
            {
                status: response.status,
                payload,
            }
        );
    }

    return parseAssistantResponsePayload(payload);
}
