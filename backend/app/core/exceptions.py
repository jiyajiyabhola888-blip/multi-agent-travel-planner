from fastapi import HTTPException, status


class TravelPlannerException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ResourceNotFoundException(TravelPlannerException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with identifier '{identifier}' was not found.",
        )


class AgentExecutionException(TravelPlannerException):
    def __init__(self, agent_name: str, reason: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent '{agent_name}' failed during execution: {reason}",
        )
