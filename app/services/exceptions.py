class DomainError(Exception):
    """Eccezione base per tutti gli errori di logica di business."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    """Sollevata quando una risorsa richiesta non esiste nel database."""


class EntityAlreadyExistsError(DomainError):
    """Sollevata quando si tenta di creare un record con un campo univoco già presente."""


class BusinessRuleViolationError(DomainError):
    """Sollevata quando un'operazione viola una regola di dominio (es. corso al completo)."""