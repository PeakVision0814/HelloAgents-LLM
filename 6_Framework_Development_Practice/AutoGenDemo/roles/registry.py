"""角色注册表与团队装配逻辑。"""

from roles.code_reviewer import create_code_reviewer
from roles.engineer import create_engineer
from roles.product_manager import create_product_manager
from roles.user_proxy import create_user_proxy


ROLE_BUILDERS = {
    "product_manager": create_product_manager,
    "engineer": create_engineer,
    "code_reviewer": create_code_reviewer,
    "user_proxy": create_user_proxy,
}

DEFAULT_ROLE_SEQUENCE = [
    "product_manager",
    "engineer",
    "code_reviewer",
    "user_proxy",
]


def build_participants(model_client, role_sequence=None):
    """根据角色序列创建团队参与者。"""
    participants = []
    sequence = role_sequence or DEFAULT_ROLE_SEQUENCE

    for role_key in sequence:
        builder = ROLE_BUILDERS.get(role_key)
        if builder is None:
            raise ValueError(f"未注册的角色: {role_key}")

        if role_key == "user_proxy":
            participants.append(builder())
        else:
            participants.append(builder(model_client))

    return participants
