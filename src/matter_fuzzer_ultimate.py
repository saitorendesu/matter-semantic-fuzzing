import subprocess
import time
import sys
import os
import random
import datetime
import string
import re

# ==========================================
# 設定: 知識ベース
# ==========================================
KNOWLEDGE_BASE = {
    "node_id": "123",
    "endpoint_id": "1",
    "cluster_level": "levelcontrol",
    "cluster_onoff": "onoff",
    "cmd_move": "move-to-level",
    # 基本の異常値シード
    "seeds": ["255", "-1", "\"\"", "\"bug\"", "None"]
}

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class MatterFuzzerUltimate:
    def __init__(self):
        self.chip_tool = "/Users/saitouren/connectedhomeip/out/debug/chip-tool"
        # 統計データ
        self.stats = {
            "total": 0, "pass": 0, "crash": 0, "bug_count": 0, 
            "unique_bugs": set(), "start": time.time()
        }
        
        # 起動チェック
        if not os.path.exists(self.chip_tool):
            print(f"{Colors.RED}Error: chip-tool not found.{Colors.ENDC}")
            sys.exit(1)

    # ---------------------------------------------------------
    # 1. 意味的ペイロード生成 (Semantic Generator)
    # ---------------------------------------------------------
    def generate_semantic_payload(self):
        """攻撃の意図(Strategy)と値(Payload)を生成"""
        if random.random() < 0.2:
            val = random.choice(KNOWLEDGE_BASE["seeds"])
            return "Known Edge Case", val
        
        attack_type = random.choice(["INT_OVERFLOW", "INT_NEGATIVE", "TYPE_MISMATCH", "FORMAT_STR", "SQL_INJECT"])
        
        if attack_type == "INT_OVERFLOW":
            val = str(255 + random.randint(0, 4000000000))
            return "Boundary Violation (High)", val
            
        elif attack_type == "INT_NEGATIVE":
            val = str(random.randint(-10000, -1))
            return "Boundary Violation (Low)", val
            
        elif attack_type == "TYPE_MISMATCH":
            length = random.randint(1, 10)
            chars = string.ascii_letters
            rand_str = ''.join(random.choice(chars) for _ in range(length))
            return "Type Mismatch (String)", f"\"{rand_str}\""
            
        elif attack_type == "FORMAT_STR":
            base = random.choice(["%s", "%x", "%n"])
            return "Format String Injection", f"\"{base * random.randint(2, 5)}\""
        
        elif attack_type == "SQL_INJECT":
            return "SQL Injection Attempt", "\"1; DROP TABLE users\""
            
        return "Unknown", "\"bug\""

    # ---------------------------------------------------------
    # 2. コマンド実行 & 解析
    # ---------------------------------------------------------
    def run_cmd(self, args, timeout=2):
        cmd = ["sudo", self.chip_tool] + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return None, "TIMEOUT"

    def extract_error_code(self, stdout):
        """ログから具体的なエラー名を抽出する (例: INVALID_DATA_TYPE)"""
        # "Error 0x000000XX: ..." のような部分を探す
        match = re.search(r"Error 0x[0-9A-Fa-f]+: (.+)", stdout)
        if match:
            return match.group(1).strip() # 具体的なエラー名
        
        # なければ一般的な失敗
        if "usage:" in stdout or "Usage:" in stdout:
            return "Usage Error (Parsing Failed)"
        return "General Failure"

    # ---------------------------------------------------------
    # 3. LED制御 (Status Monitor)
    # ---------------------------------------------------------
    def led_signal(self, state):
        target = [KNOWLEDGE_BASE["cluster_onoff"], "", KNOWLEDGE_BASE["node_id"], KNOWLEDGE_BASE["endpoint_id"]]
        try:
            if state == "PULSE":
                target[1] = "on"; self.run_cmd(target, timeout=1)
                time.sleep(0.05) # キビキビ動くように短縮
                target[1] = "off"; self.run_cmd(target, timeout=1)
            elif state == "ALERT":
                target[1] = "on"; self.run_cmd(target, timeout=1)
            elif state == "OFF":
                target[1] = "off"; self.run_cmd(target, timeout=1)
        except:
            pass # LED制御の失敗でメインを止めない

    # ---------------------------------------------------------
    # 4. ログ & レポート
    # ---------------------------------------------------------
    def log(self, type_str, msg, detail=""):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        if type_str == "PASS":
            # 正常にブロックされた理由(detail)を表示
            print(f"[{ts}] {Colors.GREEN}✅ PASS {Colors.ENDC}: {msg} -> {Colors.GREY}[{detail}]{Colors.ENDC}")
        elif type_str == "BUG":
            print(f"[{ts}] {Colors.YELLOW}⚠️  BUG  {Colors.ENDC}: {msg}")
        elif type_str == "NEW":
            print(f"[{ts}] {Colors.YELLOW}{Colors.BOLD}🏆 NEW SEMANTIC BUG! {Colors.ENDC}: {msg}")
        elif type_str == "CRASH":
            print(f"[{ts}] {Colors.RED}🚨 CRASH{Colors.ENDC}: {msg}")

    def print_summary(self):
        elapsed = str(datetime.timedelta(seconds=int(time.time() - self.stats['start'])))
        print(f"\n{Colors.CYAN}=== ULTIMATE FUZZING REPORT [Time: {elapsed}] ===")
        print(f" Total Attacks : {self.stats['total']}")
        print(f" Logic Bugs    : {self.stats['bug_count']}")
        print(f" ⭐️ Unique Semantics : {len(self.stats['unique_bugs'])}")
        print(f"=============================================={Colors.ENDC}\n")

    # ---------------------------------------------------------
    # メインループ
    # ---------------------------------------------------------
    def fuzz_one(self):
        # 毎回リセットせず、状態を維持したほうが「乗っ取られ感」が出るが、
        # ここではパルスを見せるために一旦OFFにする
        self.led_signal("OFF")
        
        # 1. 意図とペイロード生成
        strategy, val = self.generate_semantic_payload()
        disp_val = val if len(val) < 20 else val[:20] + "..."
        
        args = [KNOWLEDGE_BASE["cluster_level"], KNOWLEDGE_BASE["cmd_move"], val, "0", "0", "0", KNOWLEDGE_BASE["node_id"], KNOWLEDGE_BASE["endpoint_id"]]
        
        # 2. 実行
        out, err = self.run_cmd(args)
        self.stats["total"] += 1

        # 3. 判定ロジック
        if err == "TIMEOUT":
            self.stats["crash"] += 1
            self.log("CRASH", f"Device died on [{strategy}]: {disp_val}")
            return False

        elif out and "Success" in out:
            # 論理バグ：異常値なのに成功
            self.stats["bug_count"] += 1
            if val not in self.stats["unique_bugs"]:
                self.stats["unique_bugs"].add(val)
                self.log("NEW", f"Accepted [{strategy}]: {disp_val}")
                self.led_signal("ALERT")
                time.sleep(4) # 新種は長めにアピール
            else:
                self.log("BUG", f"Accepted [{strategy}]: {disp_val}")
                self.led_signal("ALERT")
                time.sleep(1.5)
        else:
            # 正常：エラー内容を解析して表示
            error_reason = self.extract_error_code(out if out else "")
            self.stats["pass"] += 1
            self.log("PASS", f"Blocked [{strategy}]: {disp_val}", detail=error_reason)
            self.led_signal("PULSE")
            
        return True

    def run(self):
        print(f"{Colors.BOLD}=== Matter Semantic Fuzzer (Ultimate Edition) ==={Colors.ENDC}")
        print("Target: Level Control Cluster (Reasoning & Monitoring)")
        print(f"{Colors.GREY}Initializing connection check...{Colors.ENDC}")
        
        # 起動時に一回点灯テスト
        self.led_signal("ALERT")
        time.sleep(1)
        self.led_signal("OFF")
        print("Ready. Press Ctrl+C to stop.")
        
        try:
            while True:
                if self.stats["total"] > 0 and self.stats["total"] % 10 == 0:
                    self.print_summary()

                alive = self.fuzz_one()
                
                if not alive:
                    print(f"{Colors.RED}>>> Device unresponsive. Cooldown 30s...{Colors.ENDC}")
                    time.sleep(30)
                    
                time.sleep(0.1) # 高速かつ視認可能な速度

        except KeyboardInterrupt:
            self.print_summary()
            print("Fuzzing session ended.")
        finally:
            # 安全装置: 終了時は必ずLEDを消す
            print("Cleaning up status LED...")
            self.led_signal("OFF")

if __name__ == "__main__":
    fuzzer = MatterFuzzerUltimate()
    fuzzer.run()