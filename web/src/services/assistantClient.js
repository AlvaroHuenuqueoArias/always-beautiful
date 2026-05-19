const ASSISTANT_API_BASE_URL_FALLBACK = "http://127.0.0.1:8000";
const ASSISTANT_SESSION_STORAGE_KEY =
    "always-beautiful:assistant-session-id";
const ASSISTANT_ALLOWED_CHANNELS = new Set(["web", "whatsapp", "admin"]);
const ASSISTANT_ALLOWED_TARGETS = new Set([
    "/booking",
    "/cart",
    "/products",
    "/services",
]);

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

function normalizeOptionalTarget(value) {
    if (typeof value !== "string") {
        return null;
    }

    const target = value.trim();
    const targetPath = target.split("?")[0];

    if (!ASSISTANT_ALLOWED_TARGETS.has(targetPath)) {
        return null;
    }

    return target;
}

function normalizePayload(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
        return null;
    }

    return value;
}

function normalizeQuickReply(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
        return null;
    }

    const label = typeof value.label === "string" ? value.label.trim() : "";
    const message =
        typeof value.message === "string" ? value.message.trim() : "";
    const actionType =
        typeof value.action_type === "string"
            ? value.action_type.trim()
            : "";

    if (!label || !message || !actionType) {
        return null;
    }

    return {
        label,
        message,
        actionType,
        target: normalizeOptionalTarget(value.target),
        payload: normalizePayload(value.payload),
    };
}

function parseAssistantResponsePayload(payload) {
    return {
        sessionId: payload?.session_id,
        intent: payload?.intent,
        flowStep: payload?.flow_step,
        message: payload?.message,
        requiresDeposit: Boolean(payload?.requires_deposit),
        depositPercentage: Number(payload?.deposit_percentage ?? 0),
        nextActions: Array.isArray(payload?.next_actions)
            ? payload.next_actions
            : [],
        quickReplies: Array.isArray(payload?.quick_replies)
            ? payload.quick_replies.map(normalizeQuickReply).filter(Boolean)
            : [],
        redirectTarget: normalizeOptionalTarget(payload?.redirect_target),
        cartPayload: normalizePayload(payload?.cart_payload),
        context: normalizePayload(payload?.context) || {},
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
    context,
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
            context: normalizePayload(context),
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
