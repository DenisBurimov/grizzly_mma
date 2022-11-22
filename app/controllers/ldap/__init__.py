import datetime
import ldap3
from ldap3.extend.microsoft.addMembersToGroups import (
    ad_add_members_to_groups as addUsersInGroups,
)
from ldap3.extend.microsoft.unlockAccount import ad_unlock_account

from app.controllers.ssh_ps import RemoteShell
from config import BaseConfig as config
from app.logger import log
from .user import User


class LDAP(object):
    FORMAT_USER_DN = "CN=Account {user_name},CN=Users,DC=grizzly,DC=com"
    FORMAT_GROUP_DN = "CN={group_name},DC=grizzly,DC=com"
    USERS_SEARCH_FILTER = "(&(objectClass=*)(sAMAccountName=*)(sn=*))"

    def __init__(self):
        self.LDAP_URI = f"ldap://{config.LDAP_SERVER}"
        self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL, use_ssl=True)
        # self.server = ldap3.Server(self.LDAP_URI, get_info=ldap3.ALL)
        assert self.server
        # self.connection = ldap3.Connection(self.server, user=config.LDAP_USER, password=config.LDAP_PASS)

    @property
    def users(self) -> list[User]:
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as c:
            # paged search wrapped in a generator
            entry_generator = c.extend.standard.paged_search(
                search_base=config.AD_NAME,
                search_filter=self.USERS_SEARCH_FILTER,
                search_scope=ldap3.SUBTREE,
                attributes=["*"],
                paged_size=100,
                generator=True,
            )
            for entry in entry_generator:
                if "dn" in entry and "attributes" in entry:
                    attributes = entry["attributes"]
                    yield User.parse_obj(attributes)

    def add_user(self, user_name: str, group_name: str = "Grizzly") -> User:
        user_dn = self.get_user_dn(user_name)
        group_dn = self.get_group_dn(group_name)
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as connection:
            # perform the Add operation
            success = connection.add(
                dn=user_dn,
                object_class=["top", "person", "organizationalPerson", "user"],
                attributes={
                    "sn": user_name,
                    "givenName": "Account",
                    "mail": f"{user_name}@grizzly.com",
                    "name": f"Account {user_name}",
                    "userPrincipalName": f"{user_name}@grizzly.com",
                    "sAMAccountName": user_name,
                    "accountExpires": datetime.datetime(2222, 2, 22),
                    "displayName": f"Account {user_name}",
                },
            )

            if not success:
                log(log.ERROR, "LDAP: Cannot add user [%s]", user_dn)
                log(log.ERROR, "LDAP: [%s]", connection.result)
                return None

            success = ad_unlock_account(connection, user_dn)
            if not success:
                log(log.ERROR, "LDAP: Cannot unlock [%s]", user_dn)
                log(log.ERROR, "LDAP: [%s]", connection.result)
                return None

            success = addUsersInGroups(connection, user_dn, group_dn)
            if not success:
                log(
                    log.ERROR,
                    "LDAP: Cannot add user [%s] into group [%s]",
                    user_dn,
                    group_dn,
                )
                log(log.ERROR, "LDAP: [%s]", connection.result)
                return None

        user = self.find_user_by_name(user_name)
        if user.dn == user_dn:
            log(log.INFO, "LDAP: add_user success")
            if group_dn not in user.memberOf:
                log(
                    log.ERROR,
                    "AD user [%s] does not in group [%s]",
                    user_dn,
                    group_dn,
                )
            return user
        log(log.ERROR, "LDAP: Not found LDAP user [%s]", user_dn)

    def delete_user(self, name):
        user_dn = self.get_user_dn(name)
        log(log.INFO, "LDAP: Start deleting User [%s]", user_dn)
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as connection:
            success = connection.delete(user_dn)
            if not success:
                log(log.ERROR, "LDAP: Cannot delete user [%s]", user_dn)
                log(log.ERROR, "LDAP: [%s]", connection.result)
                # temporary fix bug when we try to delete a user that has been deleted already
                if connection.result["description"] == "noSuchObject":
                    return True
                return False
        log(log.INFO, "LDAP: User [%s] was deleted successfully", user_dn)
        return True

    def change_password(self, name, new_password):
        user_dn = self.get_user_dn(name)
        sh = RemoteShell()
        res = sh.send_command(
            " ".join(
                [
                    "Set-ADAccountPassword",
                    f"-Identity '{user_dn}'",
                    "-Reset",
                    "-NewPassword",
                    f"(ConvertTo-SecureString -AsPlainText '{new_password}' -Force)",
                ]
            )
        )
        recognise_error_message = res.split("Set-ADAccountPassword :")
        if len(recognise_error_message) > 1:
            message_parts = recognise_error_message[1].split("\x1b")
            log(log.ERROR, "LDAP: [%s]", message_parts[0].strip(" \n\r\t"))
            return False
        sh.send_command(
            " ".join(["Set-ADUser", f"-Identity '{user_dn}'", "-Enabled", "$true"])
        )

        return True

    def get_group_dn(self, group_name: str) -> str:
        """
        retrieves DN by group name
        """
        return self.FORMAT_GROUP_DN.format(group_name=group_name)

    def get_user_dn(self, user_name: str) -> str:
        """retrieves DN by user name"""
        return self.FORMAT_USER_DN.format(user_name=user_name)

    def find_user_by_name(self, user_name):
        with ldap3.Connection(
            self.server, user=config.LDAP_USER, password=config.LDAP_PASS
        ) as c:
            # paged search wrapped in a generator
            entry_generator = c.extend.standard.paged_search(
                search_base=config.AD_NAME,
                search_filter=f"(&(objectClass=*)(sAMAccountName={user_name}))",
                search_scope=ldap3.SUBTREE,
                attributes=["*"],
                paged_size=100,
                generator=True,
            )
            for entry in entry_generator:
                if "dn" in entry and "attributes" in entry:
                    attributes = entry["attributes"]
                    return User.parse_obj(attributes)
