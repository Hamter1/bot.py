import nextcord
from nextcord.ext import commands
from collections import defaultdict
import asyncio
from datetime import timedelta  # datetime에서 timedelta 가져오기

intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 경고 누적 및 도배 감지에 사용할 데이터
warnings = defaultdict(int)
recent_messages = defaultdict(list)
PROHIBITED_WORDS = PROHIBITED_WORDS = [
    "간나", "갈보", "개새끼", "개자식", "개돼지", "걸레", "괴뢰", "금붕어", 
    "급식충", "김치녀", "남창", "놈", "년", "니미", "니거", "노괴", "닥쳐", 
    "당나귀 사촌", "돼지", "되놈", "두루애", "뒈지다", "등신", "딸딸이", 
    "딸피", "떨거지", "똘마니", "똘추", "똥개", "똥꼬충", "띨빵", "띨띨이", 
    "닥쳐", "다신 이세상에 내려올 생각도 하지말어", "더러운", "XX", "느금마", 
    "느개비", "니애미", "니미", "니애비", "니미럴", "니미 씨발", "느금마", "노답",
    "좆", "새끼", "병신", "좆까", "씹", "씹새끼", "씨발", "씨발놈", "병1신", "좆밥", 
    "년새끼", "찐따", "찌질이", "뻘쭈", "섹스", "뽀뽀", "쩌리", "좆밥", "쪼다", 
    "쓰레기", "개쓰레기", "개소리", "개지랄", "개판", "개차반", "거지새끼", "거렁뱅이", 
    "게이", "경을 칠 놈", "고자", "고아", "과메기", "광녀", "괴뢰군", "귓것", "그지깽깽이", 
    "금지", "급식충", "김치녀", "깝치다", "꺼벙이", "꺼져", "꼬라보다", "꼬붕", "꼰대", 
    "꼴불견", "꼴통", "굥", "남창", "냄비", "네 다음 XX", "ㄴㄷㅆ", "논다니", "뇌절", "눈깔아", 
    "니 XX", "니애미", "느금마", "느개비", "너검엄빠", "니미럴", "니미씨발", "니거", "나가 죽어", 
    "나가 뒤져", "노괴", "당나귀 사촌", "돌", "새", "빡대가리", "덜떨어지다", "돌았다", "또라이", 
    "돼지", "돼새", "두루애", "뒈지다", "등신", "돌마니", "딸딸이 부대", "땅딸보", "땡중", "떨거지", 
    "똘마니", "똘추", "똥", "똥쓰레기", "똥컴", "똥차", "똥개", "똥꼬충", "띨빵", "띨띨이", "딸피","시발", "시발놈","시발이","에미","tlqkf"
]  # 욕설 목록
SPAM_THRESHOLD = 5  # 도배 메시지 기준 개수
SPAM_INTERVAL = 10  # 도배 감지 시간(초)

# 특정 채널 ID (예시)
ALLOWED_CHANNEL_ID = 1279413694178000920 # 여기에 원하는 채널 ID를 넣으세요.

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 특정 채널에서만 동작하도록 설정
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    channel = message.channel
    user = message.author
    user_id = str(user.id)

    # 욕설 감지
    if any(word in message.content.lower() for word in PROHIBITED_WORDS):
        await message.delete()
        warning_message = await channel.send(f"{user.mention} 욕설은 나쁘니 사용하지 말아주세요!")
        warnings[user_id] += 1
        await handle_warnings(user, channel)
        await asyncio.sleep(3)  # 3초 대기 후 경고 메시지 삭제
        await warning_message.delete()
        return

    # 도배 감지
    recent_messages[user_id].append(message)
    # 특정 시간 내 메시지 수 초과 시 도배로 간주
    if len(recent_messages[user_id]) > SPAM_THRESHOLD:
        # 오래된 메시지 제거
        recent_messages[user_id] = [
            msg for msg in recent_messages[user_id]
            if (message.created_at - msg.created_at).total_seconds() <= SPAM_INTERVAL
        ]
        if len(recent_messages[user_id]) > SPAM_THRESHOLD:
            spam_message = await channel.send(f"{user.mention} 도배는 안됩니다!")
            for msg in recent_messages[user_id]:
                try:
                    await msg.delete()
                except nextcord.NotFound:
                    continue
            recent_messages[user_id] = []
            warnings[user_id] += 1
            await handle_warnings(user, channel)
            await asyncio.sleep(3)  # 3초 대기 후 도배 경고 메시지 삭제
            await spam_message.delete()
            return

# 경고 누적 처리
async def handle_warnings(user, channel):
    user_id = str(user.id)
    if warnings[user_id] >= 3:
        # 5분 타임아웃 적용
        try:
            timeout_duration = nextcord.utils.utcnow() + timedelta(minutes=5)  # datetime.timedelta 사용
            await user.timeout(timeout_duration, reason="누적 경고 3회로 인한 타임아웃")
            await channel.send(f"{user.mention} 경고 3회 누적으로 5분 타임아웃이 적용되었습니다.")
        except nextcord.Forbidden:
            await channel.send(f"{user.mention} 타임아웃을 적용할 권한이 없습니다.")
        warnings[user_id] = 0  # 경고 초기화

bot.run("")
