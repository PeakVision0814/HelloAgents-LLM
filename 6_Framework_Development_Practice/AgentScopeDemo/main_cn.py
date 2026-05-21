# -*- coding: utf-8 -*-
"""
涓夊浗鐙间汉鏉€ - 鍩轰簬AgentScope鐨勪腑鏂囩増鐙间汉鏉€娓告垙
铻嶅悎涓夊浗婕斾箟瑙掕壊鍜屼紶缁熺嫾浜烘潃鐜╂硶
"""
import asyncio
import os
import random
from typing import List, Dict, Optional

from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope.pipeline import MsgHub, sequential_pipeline, fanout_pipeline
from agentscope.formatter import OpenAIMultiAgentFormatter

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_clients import get_llm_config, load_project_env

from prompt_cn import ChinesePrompts
from game_roles import GameRoles
from structured_output_cn import (
    DiscussionModelCN,
    get_vote_model_cn,
    WitchActionModelCN,
    get_seer_model_cn,
    get_hunter_model_cn,
    WerewolfKillModelCN
)
from utils_cn import (
    check_winning_cn,
    majority_vote_cn,
    get_chinese_name,
    format_player_list,
    GameModerator,
    MAX_GAME_ROUND,
    MAX_DISCUSSION_ROUND,
)


class ThreeKingdomsWerewolfGame:
    """涓夊浗鐙间汉鏉€娓告垙涓荤被"""
    
    def __init__(self):
        self.players: Dict[str, ReActAgent] = {}
        self.roles: Dict[str, str] = {}
        self.moderator = GameModerator()
        self.alive_players: List[ReActAgent] = []
        self.werewolves: List[ReActAgent] = []
        self.villagers: List[ReActAgent] = []
        self.seer: List[ReActAgent] = []
        self.witch: List[ReActAgent] = []
        self.hunter: List[ReActAgent] = []
        
        # 濂冲帆閬撳叿鐘舵€?
        self.witch_has_antidote = True
        self.witch_has_poison = True
        
    async def create_player(self, role: str, character: str) -> ReActAgent:
        """鍒涘缓鍏锋湁涓夊浗鑳屾櫙鐨勭帺瀹?""
        name = get_chinese_name(character)
        self.roles[name] = role
        
        agent = ReActAgent(
            name=name,
            sys_prompt=ChinesePrompts.get_role_prompt(role, character),
            model=self._build_model(),`r`n            formatter=OpenAIMultiAgentFormatter(),
        )
        
        # 瑙掕壊韬唤纭
        await agent.observe(
            await self.moderator.announce(
                f"銆恵name}銆戜綘鍦ㄨ繖鍦轰笁鍥界嫾浜烘潃涓壆婕攞GameRoles.get_role_desc(role)}锛?
                f"浣犵殑瑙掕壊鏄瘂character}銆倇GameRoles.get_role_ability(role)}"
            )
        )
        
        self.players[name] = agent
        return agent
    
    async def setup_game(self, player_count: int = 6):
        """璁剧疆娓告垙"""
        print("馃幃 寮€濮嬭缃笁鍥界嫾浜烘潃娓告垙...")
        
        # 鑾峰彇瑙掕壊閰嶇疆
        roles = GameRoles.get_standard_setup(player_count)
        characters = random.sample([
            "鍒樺", "鍏崇窘", "寮犻", "璇歌憶浜?, "璧典簯",
            "鏇规搷", "鍙搁┈鎳?, "鍛ㄧ憸", "瀛欐潈"
        ], player_count)
        
        # 鍒涘缓鐜╁
        for i, (role, character) in enumerate(zip(roles, characters)):
            agent = await self.create_player(role, character)
            self.alive_players.append(agent)
            
            # 鍒嗛厤鍒板搴旈樀钀?
            if role == "鐙间汉":
                self.werewolves.append(agent)
            elif role == "棰勮█瀹?:
                self.seer.append(agent)
            elif role == "濂冲帆":
                self.witch.append(agent)
            elif role == "鐚庝汉":
                self.hunter.append(agent)
            else:
                self.villagers.append(agent)
        
        # 娓告垙寮€濮嬪叕鍛?
        await self.moderator.announce(
            f"涓夊浗鐙间汉鏉€娓告垙寮€濮嬶紒鍙備笌鑰咃細{format_player_list(self.alive_players)}"
        )
        
        print(f"鉁?娓告垙璁剧疆瀹屾垚锛屽叡{len(self.alive_players)}鍚嶇帺瀹?)
    
    async def werewolf_phase(self, round_num: int):
        """鐙间汉闃舵"""
        if not self.werewolves:
            return None
            
        await self.moderator.announce(f"馃惡 鐙间汉璇风潄鐪硷紝閫夋嫨浠婃櫄瑕佸嚮鏉€鐨勭洰鏍?..")
        
        # 鐙间汉璁ㄨ
        async with MsgHub(
            self.werewolves,
            enable_auto_broadcast=True,
            announcement=await self.moderator.announce(
                f"鐙间汉浠紝璇疯璁轰粖鏅氱殑鍑绘潃鐩爣銆傚瓨娲荤帺瀹讹細{format_player_list(self.alive_players)}"
            ),
        ) as werewolves_hub:
            # 璁ㄨ闃舵
            for _ in range(MAX_DISCUSSION_ROUND):
                for wolf in self.werewolves:
                    await wolf(structured_model=DiscussionModelCN)
            
            # 鎶曠エ鍑绘潃
            werewolves_hub.set_auto_broadcast(False)
            kill_votes = await fanout_pipeline(
                self.werewolves,
                msg=await self.moderator.announce("璇烽€夋嫨鍑绘潃鐩爣"),
                structured_model=WerewolfKillModelCN,
                enable_gather=False,
            )
            
            # 缁熻鎶曠エ
            votes = {}
            for i, vote_msg in enumerate(kill_votes):
                # 妫€鏌ote_msg鏄惁涓篘one鎴杕etadata鏄惁瀛樺湪
                if vote_msg is not None and hasattr(vote_msg, 'metadata') and vote_msg.metadata is not None:
                    votes[self.werewolves[i].name] = vote_msg.metadata.get("target")
                else:
                    # 濡傛灉杩斿洖鏃犳晥,闅忔満閫夋嫨涓€涓洰鏍?
                    print(f"鈿狅笍 {self.werewolves[i].name} 鐨勫嚮鏉€鎶曠エ鏃犳晥,闅忔満閫夋嫨鐩爣")
                    import random
                    valid_targets = [p.name for p in self.alive_players if p.name not in [w.name for w in self.werewolves]]
                    votes[self.werewolves[i].name] = random.choice(valid_targets) if valid_targets else None
            
            killed_player, _ = majority_vote_cn(votes)
            return killed_player
    
    async def seer_phase(self):
        """棰勮█瀹堕樁娈?""
        if not self.seer:
            return
            
        seer_agent = self.seer[0]
        await self.moderator.announce("馃敭 棰勮█瀹惰鐫佺溂锛岄€夋嫨瑕佹煡楠岀殑鐜╁...")
        
        check_result = await seer_agent(
            structured_model=get_seer_model_cn(self.alive_players)
        )

        # 妫€鏌ヨ繑鍥炵粨鏋滄槸鍚︽湁鏁?
        if check_result is None or not hasattr(check_result, 'metadata') or check_result.metadata is None:
            print(f"鈿狅笍 棰勮█瀹舵煡楠屽け璐?璺宠繃姝ら樁娈?)
            return

        target_name = check_result.metadata.get("target")
        if not target_name:
            print(f"鈿狅笍 棰勮█瀹舵湭閫夋嫨鏌ラ獙鐩爣,璺宠繃姝ら樁娈?)
            return

        target_role = self.roles.get(target_name, "鏉戞皯")
        
        # 鍛婄煡棰勮█瀹剁粨鏋?
        result_msg = f"鏌ラ獙缁撴灉锛歿target_name}鏄瘂'鐙间汉' if target_role == '鐙间汉' else '濂戒汉'}"
        await seer_agent.observe(await self.moderator.announce(result_msg))
    
    async def witch_phase(self, killed_player: str):
        """濂冲帆闃舵"""
        if not self.witch:
            return killed_player, None
            
        witch_agent = self.witch[0]
        await self.moderator.announce("馃鈥嶁檧锔?濂冲帆璇风潄鐪?..")
        
        # 鍛婄煡濂冲帆姝讳骸淇℃伅
        death_info = f"浠婃櫄{killed_player}琚嫾浜哄嚮鏉€" if killed_player else "浠婃櫄骞冲畨鏃犱簨"
        await witch_agent.observe(await self.moderator.announce(death_info))
        
        # 濂冲帆琛屽姩
        witch_action = await witch_agent(structured_model=WitchActionModelCN)

        saved_player = None
        poisoned_player = None

        # 妫€鏌ヨ繑鍥炵粨鏋滄槸鍚︽湁鏁?
        if witch_action is None or not hasattr(witch_action, 'metadata') or witch_action.metadata is None:
            print(f"鈿狅笍 濂冲帆琛屽姩澶辫触,瑙嗕负涓嶄娇鐢ㄦ妧鑳?)
        else:
            if witch_action.metadata.get("use_antidote") and self.witch_has_antidote:
                if killed_player:
                    saved_player = killed_player
                    self.witch_has_antidote = False
                    await witch_agent.observe(await self.moderator.announce(f"浣犱娇鐢ㄨВ鑽晳浜唟killed_player}"))

            if witch_action.metadata.get("use_poison") and self.witch_has_poison:
                poisoned_player = witch_action.metadata.get("target_name")
                if poisoned_player:
                    self.witch_has_poison = False
                    await witch_agent.observe(await self.moderator.announce(f"浣犱娇鐢ㄦ瘨鑽瘨鏉€浜唟poisoned_player}"))
        
        # 纭畾鏈€缁堟浜＄帺瀹?
        final_killed = killed_player if not saved_player else None
        
        return final_killed, poisoned_player
    
    async def hunter_phase(self, shot_by_hunter: str):
        """鐚庝汉闃舵"""
        if not self.hunter:
            return None
            
        hunter_agent = self.hunter[0]
        if hunter_agent.name == shot_by_hunter:
            await self.moderator.announce("馃徆 鐚庝汉鍙戝姩鎶€鑳斤紝鍙互甯﹁蛋涓€鍚嶇帺瀹?..")
            
            hunter_action = await hunter_agent(
                structured_model=get_hunter_model_cn(self.alive_players)
            )

            # 妫€鏌ヨ繑鍥炵粨鏋滄槸鍚︽湁鏁?
            if hunter_action is None or not hasattr(hunter_action, 'metadata') or hunter_action.metadata is None:
                print(f"鈿狅笍 鐚庝汉鎶€鑳戒娇鐢ㄥけ璐?瑙嗕负鏀惧純寮€鏋?)
                return None

            if hunter_action.metadata.get("shoot"):
                target = hunter_action.metadata.get("target")
                if target:
                    await self.moderator.announce(f"鐚庝汉{hunter_agent.name}寮€鏋甫璧颁簡{target}")
                    return target
                else:
                    print(f"鈿狅笍 鐚庝汉閫夋嫨寮€鏋絾鏈寚瀹氱洰鏍?瑙嗕负鏀惧純")
                    return None
        
        return None
    
    def update_alive_players(self, dead_players: List[str]):
        """鏇存柊瀛樻椿鐜╁鍒楄〃"""
        for dead_name in dead_players:
            if dead_name:
                # 浠庡瓨娲诲垪琛ㄧЩ闄?
                self.alive_players = [p for p in self.alive_players if p.name != dead_name]
                # 浠庡悇闃佃惀绉婚櫎
                self.werewolves = [p for p in self.werewolves if p.name != dead_name]
                self.villagers = [p for p in self.villagers if p.name != dead_name]
                self.seer = [p for p in self.seer if p.name != dead_name]
                self.witch = [p for p in self.witch if p.name != dead_name]
                self.hunter = [p for p in self.hunter if p.name != dead_name]
    
    async def day_phase(self, round_num: int):
        """鐧藉ぉ闃舵"""
        await self.moderator.day_announcement(round_num)
        
        # 璁ㄨ闃舵
        async with MsgHub(
            self.alive_players,
            enable_auto_broadcast=True,
            announcement=await self.moderator.announce(
                f"鐜板湪寮€濮嬭嚜鐢辫璁恒€傚瓨娲荤帺瀹讹細{format_player_list(self.alive_players)}"
            ),
        ) as all_hub:
            # 姣忎汉鍙戣█涓€杞?
            await sequential_pipeline(self.alive_players)
            
            # 鎶曠エ闃舵
            all_hub.set_auto_broadcast(False)
            vote_msgs = await fanout_pipeline(
                self.alive_players,
                await self.moderator.announce("璇锋姇绁ㄩ€夋嫨瑕佹窐姹扮殑鐜╁"),
                structured_model=get_vote_model_cn(self.alive_players),
                enable_gather=False,
            )
            
            # 缁熻鎶曠エ
            votes = {}
            for i, vote_msg in enumerate(vote_msgs):
                # 妫€鏌ote_msg鏄惁涓篘one鎴杕etadata鏄惁瀛樺湪
                if vote_msg is not None and hasattr(vote_msg, 'metadata') and vote_msg.metadata is not None:
                    votes[self.alive_players[i].name] = vote_msg.metadata.get("vote")
                else:
                    # 濡傛灉杩斿洖鏃犳晥,榛樿寮冪エ
                    print(f"鈿狅笍 {self.alive_players[i].name} 鐨勬姇绁ㄦ棤鏁?瑙嗕负寮冪エ")
                    votes[self.alive_players[i].name] = None
            
            voted_out, vote_count = majority_vote_cn(votes)
            await self.moderator.vote_result_announcement(voted_out, vote_count)
            
            return voted_out
    
    async def run_game(self):
        """杩愯娓告垙涓诲惊鐜?""
        try:
            await self.setup_game()
            
            for round_num in range(1, MAX_GAME_ROUND + 1):
                print(f"\n馃寵 === 绗瑊round_num}杞父鎴忓紑濮?===")
                
                # 澶滄櫄闃舵
                await self.moderator.night_announcement(round_num)
                
                # 鐙间汉鍑绘潃
                killed_player = await self.werewolf_phase(round_num)
                
                # 棰勮█瀹舵煡楠?
                await self.seer_phase()
                
                # 濂冲帆琛屽姩
                final_killed, poisoned_player = await self.witch_phase(killed_player)
                
                # 鏇存柊姝讳骸鐜╁
                night_deaths = [p for p in [final_killed, poisoned_player] if p]
                self.update_alive_players(night_deaths)
                
                # 姝讳骸鍏憡
                await self.moderator.death_announcement(night_deaths)
                
                # 妫€鏌ヨ儨鍒╂潯浠?
                winner = check_winning_cn(self.alive_players, self.roles)
                if winner:
                    await self.moderator.game_over_announcement(winner)
                    return
                
                # 鐧藉ぉ闃舵
                voted_out = await self.day_phase(round_num)
                
                # 鐚庝汉鎶€鑳?
                hunter_shot = await self.hunter_phase(voted_out)
                
                # 鏇存柊姝讳骸鐜╁
                day_deaths = [p for p in [voted_out, hunter_shot] if p]
                self.update_alive_players(day_deaths)
                
                # 妫€鏌ヨ儨鍒╂潯浠?
                winner = check_winning_cn(self.alive_players, self.roles)
                if winner:
                    await self.moderator.game_over_announcement(winner)
                    return
                
                print(f"绗瑊round_num}杞粨鏉燂紝瀛樻椿鐜╁锛歿format_player_list(self.alive_players)}")
        
        except Exception as e:
            print(f"鉂?娓告垙杩愯鍑洪敊锛歿e}")
            import traceback
            traceback.print_exc()


async def main():
    """涓诲嚱鏁?""
    # 妫€鏌ョ幆澧冨彉閲?
    if "DASHSCOPE_API_KEY" not in os.environ:
        print("鉂?璇疯缃幆澧冨彉閲?DASHSCOPE_API_KEY")
        return
    
    print("馃幃 娆㈣繋鏉ュ埌涓夊浗鐙间汉鏉€锛?)
    
    # 鍒涘缓骞惰繍琛屾父鎴?
    game = ThreeKingdomsWerewolfGame()
    await game.run_game()


if __name__ == "__main__":
    asyncio.run(main())

