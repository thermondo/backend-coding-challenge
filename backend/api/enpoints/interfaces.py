from abc import ABC

from fastapi import APIRouter


class EndPoint(ABC):
	def router(self) -> APIRouter:
		raise NotImplementedError
