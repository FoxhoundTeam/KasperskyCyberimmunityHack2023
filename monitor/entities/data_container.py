from base64 import b64decode
from typing import Any

from OpenSSL import crypto
from pydantic import BaseModel, validator

from config import settings


class DataContainer(BaseModel):
    source: str
    body: str
    signature: str

    @validator("signature")
    def check_sign(cls, value: str, values: dict[str, Any]):
        public_key = settings.source_key_map.get(values.get("source"))
        if public_key is None:
            raise ValueError("Invalid source")
        openssl_pkey = crypto.load_publickey(crypto.FILETYPE_PEM, public_key)
        cert = crypto.X509()
        cert.set_pubkey(openssl_pkey)
        data = values["body"]
        crypto.verify(cert, b64decode(value), data.encode(), "sha256")
        return value
