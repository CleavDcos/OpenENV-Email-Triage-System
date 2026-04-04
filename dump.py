import random
import uuid
from models import EmailTriageState, EmailTriageObservation, EmailTriageAction

class EmailTriageEnvironment:
    
    """Email triage environment following OpenEnv pattern."""

    # Sample dataset 
    EMAILS = [
        {
            "email": "Hi, I would like to know the pricing for your premium plan.",
            "classification": "important",
            "intent": "pricing inquiry",
            "reply": "Thank you for your interest. We will share pricing details shortly."
        },
        {
            "email": "My order hasn’t arrived yet. It’s been over a week.",
            "classification": "support",
            "intent": "complaint",
            "reply": "We’re sorry for the delay. Our support team will resolve this soon."
        },
        {
            "email": "Can I book a demo for your product next week?",
            "classification": "important",
            "intent": "booking",
            "reply": "Sure, we will schedule a demo and confirm shortly."
        },
        {
            "email": "Congratulations! You’ve won a free iPhone. Click here now!",
            "classification": "spam",
            "intent": "promotion",
            "reply": "This appears to be spam. Please avoid clicking suspicious links."
        },
        {
            "email": "The app keeps crashing when I try to open it.",
            "classification": "support",
            "intent": "complaint",
            "reply": "We're sorry for the issue. Our technical team will assist you shortly."
        },
        {
            "email": "Do you offer discounts for students?",
            "classification": "important",
            "intent": "pricing inquiry",
            "reply": "We will share information about available discounts soon."
        },
        {
            "email": "Please schedule a meeting for project discussion.",
            "classification": "important",
            "intent": "booking",
            "reply": "We will arrange a meeting and confirm the schedule shortly."
        },
        {
            "email": "Limited time offer! Get 90% off on all products!",
            "classification": "spam",
            "intent": "promotion",
            "reply": "This is likely spam. Please ignore such messages."
        },
        {
            "email": "I forgot my password and cannot log in.",
            "classification": "support",
            "intent": "complaint",
            "reply": "We will help you reset your password shortly."
        },
        {
            "email": "Is there a free trial available for your service?",
            "classification": "important",
            "intent": "pricing inquiry",
            "reply": "Yes, we will share details about the free trial shortly."
        },
        {
            "email": "Book a slot for consultation tomorrow.",
            "classification": "important",
            "intent": "booking",
            "reply": "We will confirm your consultation slot soon."
        },
        {
            "email": "Why was my payment declined? Please help.",
            "classification": "support",
            "intent": "complaint",
            "reply": "We’re sorry for the inconvenience. Our team will assist you shortly."
        }
    ]

    def __init__(self):
        self._state = EmailTriageState(
        episode_id=None,
        step_count=0,
        email_text="",
        true_classification="",
        true_intent="",
        true_reply="",
        current_stage="classification"
        )
        self._current_email = None
        self._history = []

    def reset(self, seed=None, episode_id=None) -> EmailTriageObservation:
        """Start a new episode with a random email."""
        # Set seed for reproducibility if provided
        if seed is not None:
            random.seed(seed)
        
        self._current_email = random.choice(self.EMAILS)
        self._history = []

        # Use provided episode_id or generate new one
        episode_id = episode_id or str(uuid.uuid4())
        
        self._state = EmailTriageState(
            episode_id=episode_id,  
            step_count=0,
            email_text=self._current_email["email"],
            true_classification=self._current_email["classification"],
            true_intent=self._current_email["intent"],
            true_reply=self._current_email["reply"],
            current_stage="classification"
        )

        return EmailTriageObservation(
            done=False,
            reward=0.0,
            email_text=self._state.email_text,
            current_stage="classification",
            history=[],
            message="Start with classification",
            metadata={}
        )

    def step(self, action: EmailTriageAction) -> EmailTriageObservation:
        """Process agent action."""
        #Safety check: ensure reset was called
        if not self._state or not self._state.email_text:
         return EmailTriageObservation(
            done=True, reward=0.0, email_text="", current_stage="error",
            history=[], message="Call reset() first", metadata={}
        )
        self._state.step_count += 1
        stage = self._state.current_stage
        reward = 0.0
        message = ""

        # --- Classification Stage ---
        if stage == "classification":
            if action.content == self._state.true_classification:
                reward = 0.3
                message = "Correct classification"
            else:
                message = "Wrong classification"

            self._history.append({"stage": stage, "output": action.content})
            self._state.current_stage = "intent"

        # --- Intent Stage ---
        elif stage == "intent":
            if action.content == self._state.true_intent:
                reward = 0.3
                message = "Correct intent"
            else:
                message = "Wrong intent"

            self._history.append({"stage": stage, "output": action.content})
            self._state.current_stage = "reply"

        # --- Reply Stage ---
        elif stage == "reply":
            if action.content.lower() in self._state.true_reply.lower():
                reward = 0.4
                message = "Good reply"
            else:
                reward = 0.2  # partial credit
                message = "Acceptable reply"

            self._history.append({"stage": stage, "output": action.content})

            return EmailTriageObservation(
                done=True,
                reward=reward,
                email_text=self._state.email_text,
                current_stage="done",
                history=self._history,
                message=message,
                metadata={}
            )

        return EmailTriageObservation(
            done=False,
            reward=reward,
            email_text=self._state.email_text,
            current_stage=self._state.current_stage,
            history=self._history,
            message=message,
            metadata={}
        )
    async def step_async(self, action: EmailTriageAction, **kwargs) -> EmailTriageObservation:
        return self.step(action=action)

    @property
    def state(self) -> EmailTriageState:
        return self._state
    
    async def reset_async(self, seed=None, episode_id=None) -> EmailTriageObservation:
        return self.reset(seed=seed, episode_id=episode_id)


    def close(self) -> None:
        pass
    
   


print("EmailTriageEnvironment defined.")