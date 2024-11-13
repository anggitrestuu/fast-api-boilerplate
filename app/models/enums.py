from enum import Enum

class ModelStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"

class ModelType(str, Enum):
    COMPLETION = "COMPLETION"
    CHAT = "CHAT"
    IMAGE = "IMAGE"
    EMBEDDING = "EMBEDDING"
    AUDIO = "AUDIO"

class ModelMetricType(str, Enum):
    INPUT_TOKEN = "INPUT_TOKEN"
    OUTPUT_TOKEN = "OUTPUT_TOKEN"
    IMAGE_GENERATION = "IMAGE_GENERATION"
    IMAGE_EDIT = "IMAGE_EDIT"
    IMAGE_VARIATION = "IMAGE_VARIATION"
    AUDIO_SECOND = "AUDIO_SECOND"
    AUDIO_MINUTE = "AUDIO_MINUTE"
    EMBEDDING_TOKEN = "EMBEDDING_TOKEN"

class MetricUnit(str, Enum):
    TOKENS = "TOKENS"
    CHARACTERS = "CHARACTERS"
    PIXELS = "PIXELS"
    SECONDS = "SECONDS"
    MINUTES = "MINUTES"
    REQUESTS = "REQUESTS"

class AccountStatus(str, Enum):
    """
    Status of a credit account
    
    ACTIVE: Account is fully operational
    SUSPENDED: Temporarily disabled, can be reactivated
    CLOSED: Permanently closed, cannot be reactivated
    """
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class TransactionType(str, Enum):
    """
    Type of credit transaction
    
    PURCHASE: Credit purchase transaction
    USAGE: Credit consumption from AI model usage
    REFUND: Refund of previously charged credits
    ADJUSTMENT: Manual adjustment by system admin
    """
    PURCHASE = "PURCHASE"
    USAGE = "USAGE"
    REFUND = "REFUND"
    ADJUSTMENT = "ADJUSTMENT"

class TransactionStatus(str, Enum):
    """
    Status of a credit transaction
    
    PENDING: Transaction is being processed
    COMPLETED: Transaction has been successfully processed
    FAILED: Transaction failed to process
    REVERSED: Transaction was reversed (e.g., refund or correction)
    """
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"

class PurchaseStatus(str, Enum):
    """
    Status of a credit purchase
    
    PENDING: Purchase is being processed
    COMPLETED: Purchase has been successfully completed
    FAILED: Purchase failed (e.g., payment failed)
    REFUNDED: Purchase was refunded
    """
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class TokenType(str, Enum):
    """
    Type of tokens in AI model usage
    
    INPUT: Tokens used in the input/prompt
    OUTPUT: Tokens generated in the response
    """
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"