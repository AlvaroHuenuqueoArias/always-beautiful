import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getOrCreateAssistantSessionId,
    sendAssistantMessage,
} from "../../services/assistantClient";
import AssistantChatPanel from "./AssistantChatPanel";
import AssistantComposer from "./AssistantComposer";
import AssistantMessageList from "./AssistantMessageList";

const ASSISTANT_CART_HANDOFF_STORAGE_KEY =
    "always-beautiful:assistant-cart-handoff";
const ASSISTANT_CART_DRAFT_STORAGE_KEY =
    "alwaysBeautifulAssistantCartDraft";
const ASSISTANT_CART_UPDATED_EVENT =
    "alwaysBeautifulAssistantCartUpdated";
const ASSISTANT_BOOKING_DRAFT_STORAGE_KEY =
    "alwaysBeautifulAssistantBookingDraft";
const ASSISTANT_SERVICES_FILTER_STORAGE_KEY =
    "alwaysBeautifulAssistantServicesFilter";
const ASSISTANT_CHAT_STATE_STORAGE_KEY =
    "alwaysBeautifulAssistantChatState";
const CHAT_STATE_TTL_MS = 12 * 60 * 60 * 1000;
const INACTIVITY_WARNING_MS = 120000;
const INACTIVITY_CLOSE_MS = 180000;
const EXPIRED_CHAT_RESET_DELAY_MS = 2000;
const INACTIVITY_WARNING_MESSAGE =
    "¿Sigues ahí? Cerraré este chat pronto por inactividad.";
const INACTIVITY_CLOSE_MESSAGE =
    "Cerré este chat por inactividad. Puedes abrir uno nuevo cuando quieras y seguiré ayudándote.";

const INITIAL_ASSISTANT_MESSAGE = {
    id: "assistant-welcome",
    role: "assistant",
    content:
        "Hola, soy la asistente virtual de Always Beautiful. Puedo ayudarte a reservar una hora, revisar servicios o ver productos. ¿Qué quieres hacer?",
    requiresDeposit: false,
    depositPercentage: 0,
    nextActions: [
        "La hora queda pendiente hasta confirmación del salón y abono web.",
    ],
    quickReplies: [
        {
            label: "Reservar hora",
            message: "Quiero reservar una hora",
            actionType: "reply",
            target: null,
            payload: { reason: "booking_start" },
        },
        {
            label: "Ver servicios",
            message: "Quiero ver todos los servicios disponibles",
            actionType: "navigate",
            target: "/services",
            payload: { reason: "full_services_catalog" },
        },
        {
            label: "Ver productos",
            message: "Quiero comprar productos",
            actionType: "navigate",
            target: "/products",
            payload: { reason: "product_start" },
        },
    ],
    context: {
        intent: "general",
        flow_step: "completed",
    },
};

function createMessageId(role) {
    const timestamp = Date.now().toString(36);
    const randomValue = Math.random().toString(36).slice(2, 8);

    return `${role}-${timestamp}-${randomValue}`;
}

function buildAssistantMessage(response) {
    return {
        id: createMessageId("assistant"),
        role: "assistant",
        content: response.message,
        intent: response.intent,
        flowStep: response.flowStep,
        requiresDeposit: response.requiresDeposit,
        depositPercentage: response.depositPercentage,
        nextActions: response.nextActions,
        quickReplies: response.quickReplies,
        redirectTarget: response.redirectTarget,
        cartPayload: response.cartPayload,
        context: response.context,
    };
}

function buildSystemAssistantMessage(content) {
    return {
        id: createMessageId("assistant"),
        role: "assistant",
        content,
        requiresDeposit: false,
        depositPercentage: 0,
        nextActions: [],
        quickReplies: [],
        context: {},
    };
}

function readJsonStorageItem(key) {
    const storage = globalThis.sessionStorage;

    if (!storage) {
        return null;
    }

    try {
        return JSON.parse(storage.getItem(key));
    } catch {
        return null;
    }
}

function isPlainObject(value) {
    return Boolean(
        value && typeof value === "object" && !Array.isArray(value)
    );
}

function getInitialChatState() {
    const storedState = readJsonStorageItem(ASSISTANT_CHAT_STATE_STORAGE_KEY);
    const now = Date.now();
    const storedContext = isPlainObject(storedState?.context)
        ? storedState.context
        : INITIAL_ASSISTANT_MESSAGE.context;

    if (
        !isPlainObject(storedState) ||
        typeof storedState.lastInteractionAt !== "number" ||
        now - storedState.lastInteractionAt > CHAT_STATE_TTL_MS
    ) {
        return {
            messages: [INITIAL_ASSISTANT_MESSAGE],
            context: INITIAL_ASSISTANT_MESSAGE.context,
            lastInteractionAt: now,
            warningShown: false,
            closedByInactivity: false,
            isExpired: false,
            inputDisabled: false,
            expiredAt: null,
            conversationLocked: Boolean(storedContext.conversation_locked),
        };
    }

    return {
        messages: Array.isArray(storedState.messages)
            ? storedState.messages
            : [INITIAL_ASSISTANT_MESSAGE],
        context: isPlainObject(storedState.context)
            ? storedState.context
            : INITIAL_ASSISTANT_MESSAGE.context,
        lastInteractionAt: storedState.lastInteractionAt,
        warningShown: Boolean(storedState.warningShown),
        closedByInactivity: Boolean(storedState.closedByInactivity),
        isExpired: Boolean(storedState.isExpired),
        inputDisabled: Boolean(storedState.inputDisabled),
        expiredAt:
            typeof storedState.expiredAt === "number"
                ? storedState.expiredAt
                : null,
        conversationLocked: Boolean(storedContext.conversation_locked),
    };
}

function persistCartHandoff(cartPayload) {
    if (!cartPayload) {
        return;
    }

    const storage = globalThis.sessionStorage;

    if (!storage) {
        return;
    }

    storage.setItem(
        ASSISTANT_CART_HANDOFF_STORAGE_KEY,
        JSON.stringify(cartPayload)
    );
    notifyAssistantCartChange();
}

function buildAssistantCartDraft(context) {
    if (!isPlainObject(context)) {
        return null;
    }

    const cartItems = Array.isArray(context.cart_items)
        ? context.cart_items.filter((item) => typeof item === "string" && item)
        : [];
    const cartCount = cartItems.length;

    if (cartCount <= 0) {
        return null;
    }

    return {
        source: "assistant",
        cart_count: cartCount,
        cart_items: cartItems,
    };
}

function persistAssistantCartDraft(context) {
    const cartDraft = buildAssistantCartDraft(context);

    if (!cartDraft) {
        return;
    }

    const storage = globalThis.sessionStorage;

    if (!storage) {
        return;
    }

    storage.setItem(
        ASSISTANT_CART_DRAFT_STORAGE_KEY,
        JSON.stringify(cartDraft)
    );
    notifyAssistantCartChange();
}

function buildBookingDraft(context) {
    if (!context || typeof context !== "object" || Array.isArray(context)) {
        return null;
    }

    const hasBookingSignal =
        context.intent === "booking" ||
        context.selected_professional ||
        context.selected_service ||
        context.requested_day ||
        context.requested_time;

    if (!hasBookingSignal) {
        return null;
    }

    return {
        source: "assistant",
        intent: "booking",
        flow_step: context.flow_step || null,
        selected_professional: context.selected_professional || null,
        professional_id: context.professional_id || null,
        professional_role: context.professional_role || null,
        selected_service: context.selected_service || null,
        requested_day: context.requested_day || null,
        requested_time: context.requested_time || null,
        deposit_required: context.deposit_required ?? true,
        deposit_percentage: context.deposit_percentage ?? 20,
    };
}

function persistBookingDraft(context) {
    const bookingDraft = buildBookingDraft(context);

    if (!bookingDraft) {
        return;
    }

    const storage = globalThis.sessionStorage;

    if (!storage) {
        return;
    }

    storage.setItem(
        ASSISTANT_BOOKING_DRAFT_STORAGE_KEY,
        JSON.stringify(bookingDraft)
    );
}

function buildServicesFilter(context) {
    if (!isPlainObject(context)) {
        return null;
    }

    const hasServicesSignal =
        context.selected_professional ||
        context.professional_id ||
        context.selected_service ||
        context.reason;

    if (!hasServicesSignal) {
        return {
            source: "assistant",
            reason: "full_services_catalog",
        };
    }

    return {
        source: "assistant",
        reason: context.reason || "assistant_services_navigation",
        selected_professional: context.selected_professional || null,
        professional_id: context.professional_id || null,
        professional_role: context.professional_role || null,
        selected_service: context.selected_service || null,
    };
}

function persistServicesFilter(context) {
    const servicesFilter = buildServicesFilter(context);

    if (!servicesFilter) {
        return;
    }

    const storage = globalThis.sessionStorage;

    if (!storage) {
        return;
    }

    storage.setItem(
        ASSISTANT_SERVICES_FILTER_STORAGE_KEY,
        JSON.stringify(servicesFilter)
    );
}

function clearAssistantFlowStorage() {
    const storage = globalThis.sessionStorage;

    if (!storage) {
        return;
    }

    storage.removeItem(ASSISTANT_CART_HANDOFF_STORAGE_KEY);
    storage.removeItem(ASSISTANT_CART_DRAFT_STORAGE_KEY);
    storage.removeItem(ASSISTANT_BOOKING_DRAFT_STORAGE_KEY);
    storage.removeItem(ASSISTANT_SERVICES_FILTER_STORAGE_KEY);
    notifyAssistantCartChange();
}

function notifyAssistantCartChange() {
    globalThis.dispatchEvent?.(new Event(ASSISTANT_CART_UPDATED_EVENT));
}

function getTargetPath(target) {
    return typeof target === "string" ? target.split("?")[0] : "";
}

function navigateToTarget(target, navigate) {
    if (!target) {
        return;
    }

    if (target.startsWith("/") && typeof navigate === "function") {
        navigate(target);
        return;
    }

    globalThis.location?.assign?.(target);
}

function isCompleteCartPayload(cartPayload) {
    const items = Array.isArray(cartPayload?.items) ? cartPayload.items : [];
    const hasValidItems =
        items.length > 0 &&
        items.every(
            (item) =>
                item?.professional &&
                item?.professional_id &&
                item?.professional_role &&
                item?.service_label &&
                item?.deposit_percentage === 20 &&
                item?.remaining_percentage === 80 &&
                item?.amount_status === "pending_final_price"
        );
    const hasValidScheduleStatus =
        cartPayload?.schedule_status === "pending_selection" ||
        cartPayload?.schedule_status === "pending_confirmation";
    const hasValidScheduleDetail =
        cartPayload?.schedule_status === "pending_confirmation"
            ? Boolean(cartPayload?.requested_day && cartPayload?.requested_time)
            : true;

    return Boolean(
        cartPayload?.type === "booking_deposit" &&
            cartPayload?.status === "pending_deposit" &&
            cartPayload?.deposit_percentage === 20 &&
            cartPayload?.remaining_percentage === 80 &&
            cartPayload?.service_label &&
            cartPayload?.professional_label &&
            cartPayload?.selected_service &&
            cartPayload?.selected_professional &&
            cartPayload?.professional_id &&
            cartPayload?.professional_role &&
            hasValidItems &&
            hasValidScheduleStatus &&
            hasValidScheduleDetail &&
            cartPayload?.confirmation_status === "not_confirmed" &&
            cartPayload?.payment_status === "deposit_pending"
    );
}

function getPayloadContext(payload) {
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
        return {};
    }

    const { context, ...payloadFields } = payload;
    const payloadContext =
        context && typeof context === "object" && !Array.isArray(context)
            ? context
            : {};

    return {
        ...payloadContext,
        ...payloadFields,
    };
}

function mergeContext(...contexts) {
    return contexts.reduce(
        (mergedContext, context) => ({
            ...mergedContext,
            ...(context && typeof context === "object" && !Array.isArray(context)
                ? context
                : {}),
        }),
        {}
    );
}

function isRestartMessage(message) {
    return message.trim().toLowerCase() === "volver a iniciar";
}

export default function AssistantChatWidget({ isOpen = false, onClose }) {
    const navigate = useNavigate();
    const initialChatState = useRef(getInitialChatState());
    const expiredResetTimerRef = useRef(null);
    const [messages, setMessages] = useState(initialChatState.current.messages);
    const [draftMessage, setDraftMessage] = useState("");
    const [conversationContext, setConversationContext] = useState(
        initialChatState.current.context
    );
    const [activityVersion, setActivityVersion] = useState(0);
    const [lastInteractionAt, setLastInteractionAt] = useState(
        initialChatState.current.lastInteractionAt
    );
    const [warningShown, setWarningShown] = useState(
        initialChatState.current.warningShown
    );
    const [closedByInactivity, setClosedByInactivity] = useState(
        initialChatState.current.closedByInactivity
    );
    const [isExpired, setIsExpired] = useState(
        initialChatState.current.isExpired
    );
    const [inputDisabled, setInputDisabled] = useState(
        initialChatState.current.inputDisabled
    );
    const [conversationLocked, setConversationLocked] = useState(
        Boolean(initialChatState.current.conversationLocked)
    );
    const [expiredAt, setExpiredAt] = useState(initialChatState.current.expiredAt);
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    function resetInactivityTimer() {
        setLastInteractionAt(Date.now());
        setWarningShown(false);
        setClosedByInactivity(false);
        setIsExpired(false);
        setInputDisabled(false);
        setConversationLocked(false);
        setExpiredAt(null);
        setActivityVersion((currentValue) => currentValue + 1);
    }

    function resetConversationForNewChat() {
        if (expiredResetTimerRef.current) {
            globalThis.clearTimeout(expiredResetTimerRef.current);
            expiredResetTimerRef.current = null;
        }

        clearAssistantFlowStorage();
        setMessages([INITIAL_ASSISTANT_MESSAGE]);
        setConversationContext(INITIAL_ASSISTANT_MESSAGE.context);
        setWarningShown(false);
        setClosedByInactivity(false);
        setIsExpired(false);
        setInputDisabled(false);
        setExpiredAt(null);
        setLastInteractionAt(Date.now());
        setActivityVersion((currentValue) => currentValue + 1);
    }

    function scheduleExpiredChatReset() {
        if (!isExpired || expiredResetTimerRef.current) {
            return;
        }

        expiredResetTimerRef.current = globalThis.setTimeout(() => {
            expiredResetTimerRef.current = null;
            resetConversationForNewChat();
        }, EXPIRED_CHAT_RESET_DELAY_MS);
    }

    useEffect(() => {
        if (isOpen) {
            if (closedByInactivity) {
                return;
            }

            resetInactivityTimer();
        }
    }, [isOpen]);

    useEffect(() => {
        if (!isOpen || isExpired) {
            return undefined;
        }

        const elapsedMs = Date.now() - lastInteractionAt;
        const warningDelayMs = Math.max(0, INACTIVITY_WARNING_MS - elapsedMs);
        const closeDelayMs = Math.max(0, INACTIVITY_CLOSE_MS - elapsedMs);
        const warningTimer = warningShown
            ? null
            : globalThis.setTimeout(() => {
                  setMessages((currentMessages) => [
                      ...currentMessages,
                      buildSystemAssistantMessage(INACTIVITY_WARNING_MESSAGE),
                  ]);
                  setWarningShown(true);
              }, warningDelayMs);
        const closeTimer = globalThis.setTimeout(() => {
            clearAssistantFlowStorage();
            setConversationContext(INITIAL_ASSISTANT_MESSAGE.context);
            setMessages((currentMessages) => [
                ...currentMessages,
                buildSystemAssistantMessage(INACTIVITY_CLOSE_MESSAGE),
            ]);
            setClosedByInactivity(true);
            setIsExpired(true);
            setInputDisabled(true);
            setConversationLocked(false);
            setExpiredAt(Date.now());
        }, closeDelayMs);

        return () => {
            if (warningTimer) {
                globalThis.clearTimeout(warningTimer);
            }
            globalThis.clearTimeout(closeTimer);
            if (expiredResetTimerRef.current) {
                globalThis.clearTimeout(expiredResetTimerRef.current);
                expiredResetTimerRef.current = null;
            }
        };
    }, [activityVersion, isExpired, isOpen, lastInteractionAt, warningShown]);

    useEffect(() => {
        const storage = globalThis.sessionStorage;

        if (!storage) {
            return;
        }

        storage.setItem(
            ASSISTANT_CHAT_STATE_STORAGE_KEY,
            JSON.stringify({
                messages,
                context: conversationContext,
                isOpen,
                lastInteractionAt,
                warningShown,
                closedByInactivity,
                isExpired,
                inputDisabled,
                conversationLocked,
                expiredAt,
            })
        );
    }, [
        messages,
        conversationContext,
        isOpen,
        lastInteractionAt,
        warningShown,
        closedByInactivity,
        isExpired,
        inputDisabled,
        conversationLocked,
        expiredAt,
    ]);

    async function handleSubmit(message, options = {}) {
        const trimmedMessage = message.trim();
        const requestContext = mergeContext(
            conversationContext,
            options.context
        );
        const displayContent =
            typeof options.displayContent === "string" &&
            options.displayContent.trim()
                ? options.displayContent.trim()
                : trimmedMessage;

        if (!trimmedMessage || isLoading || inputDisabled || isExpired) {
            return null;
        }

        resetInactivityTimer();

        const userMessage = {
            id: createMessageId("user"),
            role: "user",
            content: displayContent,
            requiresDeposit: false,
            depositPercentage: 0,
            nextActions: [],
            quickReplies: [],
            context: requestContext,
        };

        setMessages((currentMessages) => [...currentMessages, userMessage]);
        setDraftMessage("");
        setErrorMessage("");
        setIsLoading(true);

        try {
            const response = await sendAssistantMessage({
                sessionId: getOrCreateAssistantSessionId(),
                message: trimmedMessage,
                context: requestContext,
            });
            const assistantMessage = buildAssistantMessage(response);
            const isRestart = isRestartMessage(trimmedMessage);

            if (isRestart) {
                clearAssistantFlowStorage();
                setConversationContext(response.context || {});
                setMessages([assistantMessage]);
                setConversationLocked(
                    Boolean(response.context?.conversation_locked)
                );
            } else if (response.context?.cart_redirected) {
                setConversationContext(
                    mergeContext(requestContext, response.context)
                );
                setMessages([assistantMessage]);
                setConversationLocked(true);
            } else {
                setConversationContext(
                    mergeContext(requestContext, response.context)
                );
                setMessages((currentMessages) => [
                    ...currentMessages,
                    assistantMessage,
                ]);
                persistAssistantCartDraft(response.context);
                setConversationLocked(
                    Boolean(response.context?.conversation_locked)
                );
            }

            if (response.cartPayload) {
                persistCartHandoff(response.cartPayload);
            }

            return response;
        } catch {
            setErrorMessage(
                "No pudimos contactar al asistente en este momento. Intenta nuevamente desde la web en unos minutos."
            );

            return null;
        } finally {
            setIsLoading(false);
        }
    }

    async function handleQuickReply(quickReply) {
        if (inputDisabled || isExpired) {
            return;
        }

        const quickReplyContext = mergeContext(
            conversationContext,
            getPayloadContext(quickReply.payload)
        );
        const response = await handleSubmit(quickReply.message, {
            displayContent: quickReply.label,
            context: quickReplyContext,
        });

        if (!response || !quickReply.target) {
            return;
        }

        if (quickReply.actionType === "cart_handoff" && quickReply.target === "/cart") {
            const cartPayload =
                response.cartPayload || quickReply.payload?.cart_payload;

            if (
                response.redirectTarget === "/cart" &&
                isCompleteCartPayload(cartPayload)
            ) {
                persistCartHandoff(cartPayload);
                resetInactivityTimer();
                navigateToTarget("/cart", navigate);
            }

            return;
        }

        if (quickReply.actionType === "navigate") {
            const targetPath = getTargetPath(quickReply.target);
            const navigationContext = mergeContext(
                quickReplyContext,
                response.context
            );

            if (targetPath === "/booking") {
                persistBookingDraft(navigationContext);
            }

            if (targetPath === "/services") {
                persistServicesFilter(navigationContext);
            }

            resetInactivityTimer();
            navigateToTarget(quickReply.target, navigate);
        }
    }

    return (
        <AssistantChatPanel isOpen={isOpen} onClose={onClose}>
            <div
                className="assistant-chat-widget__session"
                onMouseEnter={scheduleExpiredChatReset}
                onClick={scheduleExpiredChatReset}
            >
                <AssistantMessageList
                    messages={messages}
                    onQuickReply={handleQuickReply}
                    disabled={inputDisabled || isExpired}
                />

                {isLoading && (
                    <p className="assistant-chat-widget__status" aria-live="polite">
                        El asistente está preparando una respuesta.
                    </p>
                )}

                {errorMessage && (
                    <p className="assistant-chat-widget__error" role="alert">
                        {errorMessage}
                    </p>
                )}

                <AssistantComposer
                    value={draftMessage}
                    onChange={(value) => {
                        setDraftMessage(value);
                        resetInactivityTimer();
                    }}
                    onSubmit={handleSubmit}
                    disabled={
                        isLoading ||
                        inputDisabled ||
                        isExpired ||
                        conversationLocked
                    }
                />
            </div>
        </AssistantChatPanel>
    );
}
