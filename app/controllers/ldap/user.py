""" AD User """

from datetime import datetime
from uuid import UUID
from typing import Optional

import ldap3
from pydantic import BaseModel, Field

from app.controllers.ssh_ps import RemoteShell
from config import BaseConfig as config

LDAP_URI = f"ldap://{config.LDAP_SERVER}"


class User(BaseModel):
    objectClass: list[str]
    dn: str = Field(alias="distinguishedName")
    mail: Optional[str]
    cn: str
    sn: str
    givenName: str
    instanceType: int
    whenCreated: datetime
    whenChanged: datetime
    displayName: Optional[str]
    memberOf: Optional[list[str]] = []
    uSNChanged: int
    name: str
    objectGUID: UUID
    userAccountControl: int
    badPwdCount: int
    codePage: int
    badPasswordTime: datetime
    lastLogon: datetime
    pwdLastSet: datetime
    primaryGroupID: int
    objectSid: str
    accountExpires: datetime
    logonCount: int
    sAMAccountName: str
    sAMAccountType: int
    userPrincipalName: str
    lockoutTime: Optional[datetime]
    objectCategory: str

    def delete(self):
        """delete the AD user"""
        self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL)
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as connection:
            connection.delete(self.dn)

    def reset_password(self, new_pass: str):
        new_pass = self.secure_posh_str(new_pass)
        """reset user password

        Args:
            new_pass (str): the new password

        Returns:
            bool: True if operation succeeded
        """
        # flake8: noqa E501
        # posh: Set-ADAccountPassword -Identity "CN=Account CYF787,CN=Users,DC=kryptr,DC=li" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "Simple2B123" -Force)
        sh = RemoteShell()
        res = sh.send_command(
            " ".join(
                [
                    "Set-ADAccountPassword",
                    f"-Identity '{self.dn}'",
                    "-Reset",
                    "-NewPassword",
                    f"(ConvertTo-SecureString -AsPlainText '{new_pass}' -Force)",
                ]
            )
        )
        recognize_error_message = res.split("Set-ADAccountPassword :")
        if len(recognize_error_message) > 1:
            message_parts = recognize_error_message[1].split("\x1b")
            return message_parts[0].strip(" \n\r\t")
        sh.send_command(
            " ".join(["Set-ADUser", f"-Identity '{self.dn}'", "-Enabled", "$true"])
        )
        return ""

    @staticmethod
    def secure_posh_str(value: str):
        return value.replace("'", r"\'")
