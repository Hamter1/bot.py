from googletrans import Translator
import nextcord
from nextcord.ext import commands
import requests
import random
import psutil
import time
from nextcord import Interaction
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import asyncio
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View
import os
import sys
import aiohttp

# 봇 인스턴스 생성
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
# 상태 메시지를 주기적으로 변경하는 코루틴 함수
async def change_status():
    while True:
        # 첫 번째 길드의 멤버 수 가져오기
        if bot.guilds:  # 길드가 존재하는지 확인
            member_count = sum(1 for _ in bot.guilds[0].members)  # 첫 번째 길드의 멤버 수 계산
            server_count = len(bot.guilds)  # 전체 서버 수 계산
        else:
            member_count = 0
            server_count = 0

        # 상태 메시지 목록
        status_messages = [
            f'👥 {member_count}명한테 도움을 주는 중...',
            f'🌐 {server_count}개의 서버에서 일을 하고 있습니다...',
            '🚀 로켓처럼 빠르게...',
            '🔄 강제 업데이트 중...',
            '🛠️ 테스트 중 지금까지 실패한게 10억 9천 9백만...',
        ]

        # 상태 메시지를 주기적으로 변경
        for message in status_messages:
            activity = nextcord.Activity(type=nextcord.ActivityType.playing, name=message)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(10)  # 10초 대기


# 봇이 준비되었을 때 호출되는 이벤트
@bot.event
async def on_ready():
    print(f'🤖 {bot.user}으로 로그인되었습니다! (ID: {bot.user.id})')
    # 상태 메시지를 주기적으로 변경하는 코루틴 시작
    bot.loop.create_task(change_status())


# 사용자 호감도 저장
user_affinity = {}

# 간단한 대화 규칙 정의
responses = {
    "안녕": "안녕하세요! 어떻게 도와드릴까요?",
    "잘 지내?": "네, 잘 지내고 있어요! 당신은요?",
    "이름이 뭐야?": "저는 루미나에요. 만나서 반가워요!",
    "고마워": "천만에요! 도움이 되어 기뻐요."
}


# 봇 정보 명령어 정의
@bot.slash_command(name='봇정보', description='봇 및 서버 정보를 보여줍니다.')
async def info(interaction: nextcord.Interaction):
    server = interaction.guild
    uptime = os.popen('uptime -p').read().strip().replace('weeks', '주').replace('days', '일').replace('hours', '시간').replace('minutes', '분')
    python_version = subprocess.check_output(['python', '--version']).decode('utf-8').strip()
    
    modules = subprocess.check_output(['pip', 'freeze']).decode('utf-8').strip().split('\n')
    limited_modules = '\n'.join(modules[:10])  # 상위 10개 모듈만 표시

    embed = nextcord.Embed(title='봇 정보', color=0x1abc9c)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    embed.add_field(name='서버 이름', value=server.name, inline=False)
    embed.add_field(name='서버 ID', value=server.id, inline=False)
    embed.add_field(name='봇이 들어간 수', value=len(bot.guilds), inline=False)
    embed.add_field(name='봇 업타임', value=uptime, inline=False)
    embed.add_field(name='개발자', value='<@aru_0319>', inline=False)
    embed.add_field(name='시스템 정보', value=f'OS: {os.uname().sysname} {os.uname().release}\nPython 버전: {python_version}\n모듈:\n```\n{limited_modules}\n```', inline=False)

    await interaction.send(embed=embed)
@bot.slash_command(name="개발현황", description="개발 현황을 말합니다.")
async def development_status(interaction: nextcord.Interaction):
    await interaction.response.send_message("일시 중단")
    
# 게임 정보 명령어 정의
@bot.slash_command(name='게임순위', description='인기 게임의 최신 정보를 제공합니다.')
async def gameinfo(interaction: nextcord.Interaction):
    # 예시로 게임메카의 인기 게임 순위를 가져오는 코드
    url = 'https://www.gamemeca.com/ranking.php'
    response = requests.get(url)
    if response.status_code == 200:
        # 웹 페이지에서 필요한 정보를 추출하는 코드 (예시)
        game_info = "인기 게임 순위:\n1. 리그 오브 레전드\n2. 발로란트\n3. FC 온라인\n..."
        embed = nextcord.Embed(title="인기 게임 정보", description=game_info, color=nextcord.Color.green())
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('게임 정보를 가져오는 데 실패했습니다.')
        
@bot.slash_command(name='Translate', description='Translate text')
async def translate(interaction: nextcord.Interaction, text: str, dest: str):
    valid_languages = ['en', 'ko', 'ja', 'fr', 'de', 'ru'] 
    if dest in valid_languages:
        translation = GoogleTranslator(source='auto', target=dest).translate(text)
        await interaction.response.send_message(translation)
    else:
        await interaction.response.send_message('Invalid target language.')

@bot.slash_command(name='번역기', description='텍스트를 번역합니다.')
async def translate(interaction: nextcord.Interaction, text: str, dest: str):
    valid_languages = ['en', 'ko', 'ja', 'fr', 'de', 'ru'] 
    if dest in valid_languages:
        translation = GoogleTranslator(source='auto', target=dest).translate(text)
        await interaction.response.send_message(translation)
    else:
        await interaction.response.send_message('유효하지 않은 대상 언어입니다.')

# 서버 정보 명령어 정의
@bot.slash_command(name='서버정보', description='서버의 정보를 표시합니다.')
async def serverinfo(interaction: nextcord.Interaction):
    guild = interaction.guild
    embed = nextcord.Embed(title=f"{guild.name} 서버 정보", color=nextcord.Color.purple())
    embed.add_field(name="서버 이름", value=guild.name, inline=False)
    embed.add_field(name="서버 ID", value=guild.id, inline=False)
    embed.add_field(name="서버 생성일", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="서버 멤버 수", value=guild.member_count, inline=False)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="핑", description="핑을 확인합니다.")
async def ping(interaction: nextcord.Interaction):
    start_time = time.time()
    await interaction.response.send_message("퐁!")
    end_time = time.time()
    rest_ping = round((end_time - start_time) * 1000)
    gateway_ping = round(bot.latency * 1000)
    
    embed = nextcord.Embed(title="핑 정보", color=nextcord.Color.blue())
    embed.add_field(name="루미나가 받아 치는데에 걸린 시간입니다!", value="REST 핑: {}ms\nGateway 핑: {}ms".format(rest_ping, gateway_ping), inline=False)
    
    await interaction.edit_original_message(embed=embed)

@bot.slash_command(name="사용량", description="서버의 CPU, RAM 및 디스크 사용량을 확인합니다")
async def usage(interaction: nextcord.Interaction):
    # CPU 사용량
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # RAM 사용량
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 3)  # GB 단위로 변환
    used_memory = memory_info.used / (1024 ** 3)  # GB 단위로 변환
    available_memory = memory_info.available / (1024 ** 3)  # GB 단위로 변환

    # 디스크 사용량
    disk_info = psutil.disk_usage('/')
    total_disk = disk_info.total / (1024 ** 3)  # GB 단위로 변환
    used_disk = disk_info.used / (1024 ** 3)  # GB 단위로 변환
    free_disk = disk_info.free / (1024 ** 3)  # GB 단위로 변환

    # 결과 메시지 생성
    result_message = (
        f"**CPU 사용량**: {cpu_usage}%\n"
        f"**전체 RAM**: {total_memory:.2f} GB\n"
        f"**사용된 RAM**: {used_memory:.2f} GB\n"
        f"**사용 가능한 RAM**: {available_memory:.2f} GB\n"
        f"**전체 디스크**: {total_disk:.2f} GB\n"
        f"**사용된 디스크**: {used_disk:.2f} GB\n"
        f"**남은 디스크**: {free_disk:.2f} GB"
    )

    # 결과 메시지 전송
    await interaction.response.send_message(result_message)

# 가위바위보 슬래시 커맨드 추가
@bot.slash_command(name="가위바위보", description="가위바위보 게임을 합니다.")
async def rps(interaction: nextcord.Interaction, user_choice: str):
    choices = ['가위', '바위', '보']
    bot_choice = random.choice(choices)
    result = determine_winner(user_choice, bot_choice)
    await interaction.response.send_message(f'당신의 선택: {user_choice}\n루미나의 선택: {bot_choice}\n결과: {result}')

def determine_winner(user, bot):
    if user == bot:
        return '무승부!'
    elif (user == '가위' and bot == '보') or (user == '바위' and bot == '가위') or (user == '보' and bot == '바위'):
        return '당신이 이겼습니다!'
    else:
        return '루미나가 이겼습니다!'


@bot.slash_command(name="아루님이_좋아하는_노래", description="아루님의 좋아하는 노래를 보여줍니다.")
async def favorite_song(interaction: Interaction):
    embed = nextcord.Embed(title="아루님의_좋아하는_노래", description="아이리칸나 최종화", color=0x00ff00)
    embed.set_thumbnail(url="https://ifh.cc/g/mhWStJ.jpg")
    embed.add_field(name="아티스트", value="아이리 칸나", inline=False)
    embed.add_field(name="앨범", value="최종화", inline=False)
    embed.add_field(name="노래 링크", value="https://youtu.be/ajDAmJYPQ-U?si=qDm8pYC5THALRUrZ", inline=False)
    await interaction.response.send_message(embed=embed)

# 특정 사용자 ID를 설정합니다.
AUTHORIZED_USER_ID = 960873072225833010

@bot.slash_command(name="점검공지", description="점검 공지를 설정합니다")
async def maintenance(interaction: Interaction, time: str = SlashOption(description="점검 시작 시간 (HH:MM)")):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("이 명령어를 사용할 권한이 없습니다.", ephemeral=True)
        return

    start_time = datetime.strptime(time, "%H:%M").time()
    now = datetime.now().time()
    remaining_time = (datetime.combine(datetime.today(), start_time) - datetime.combine(datetime.today(), now)).total_seconds()

    if remaining_time < 0:
        await interaction.response.send_message("시작 시간이 현재 시간보다 이전입니다. 다시 설정해주세요.")
        return

    await interaction.response.send_message(f"봇이 {time}에 점검을 시작합니다.")
    
    await asyncio.sleep(remaining_time)
    await interaction.channel.send(f"점검이 시작되었습니다. 봇을 종료합니다.")
    await bot.close()

@bot.slash_command(name="도움말", description="도움말을 말해줘요!")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="안녕하세요, 루미나입니다!",
        description="저는 다양한 기능을 제공하는 디스코드 봇입니다. 현재는 기능이 많지 않지만, 점차 업데이트될 예정입니다!",
        color=nextcord.Colour.purple()
    )
    embed.add_field(
        name="!명령어",
        value=(
            "`!도움말` - 도움말을 표시합니다."
        ),
        inline=False
    )
    embed.add_field(
        name="/명령어",
        value=(
            "`/가위바위보` - 가위바위보 게임을 합니다.\n"
            "`/개발현황` - 개발 현황을 알려줍니다.\n"
            "`/게임순위` - 인기 게임 순위를 제공합니다.\n"
            "`/번역기` - 텍스트를 번역합니다.\n"
            "`/봇정보` - 봇 정보를 보여줍니다.\n"
            "`/사용량` - 서버의 CPU, RAM 및 디스크 사용량을 확인합니다.\n"
            "`/서버정보` - 서버 정보를 표시합니다.\n"
            "`/도움말` - 도움말을 말해줘요.\n"
			"`/하트` - 루미나의 한디리 하트 사이트로 이동합니다.\n"
            "`/초대` - 루미나의 초대 사이트로 이동합니다."
        ),
        inline=False
    )
    embed.set_footer(text="루미나 봇과 함께 즐거운 시간 되세요!")
    
    await interaction.response.send_message(embed=embed)

@bot.command(name="도움말")
async def help_command(ctx):
    embed = nextcord.Embed(
        title="안녕하세요, 루미나입니다!",
        description="저는 다양한 기능을 제공하는 디스코드 봇입니다. 현재는 기능이 많지 않지만, 점차 업데이트될 예정입니다!",
        color=nextcord.Colour.purple()
    )
    embed.add_field(
        name="!명령어",
        value="`!도움말` - 도움말을 표시합니다.",
        inline=False
    )
    embed.add_field(
        name="/명령어",
        value=(
            "`/가위바위보` - 가위바위보 게임을 합니다.\n"
            "`/개발현황` - 개발 현황을 알려줍니다.\n"
            "`/게임순위` - 인기 게임 순위를 제공합니다.\n"
            "`/번역기` - 텍스트를 번역합니다.\n"
            "`/봇정보` - 봇 정보를 보여줍니다.\n"
            "`/사용량` - 서버의 CPU, RAM 및 디스크 사용량을 확인합니다.\n"
            "`/서버정보` - 서버 정보를 표시합니다.\n"
            "`/도움말` - 도움말을 말해줘요.\n"
			"`/하트` - 루미나의 한디리 하트 사이트로 이동합니다.\n"
            "`/초대` - 루미나의 초대 사이트로 이동합니다."
        ),
        inline=False
    )
    embed.set_footer(text="루미나 봇과 함께 즐거운 시간 되세요!")
    
    await ctx.send(embed=embed)    

@bot.slash_command(name="하트", description="루미나의 한디리 하트 사이트로 이동합니다.")
async def heart_command(interaction: nextcord.Interaction):
    await interaction.response.send_message("루미나의 :heart:[하트](https://koreanbots.dev/bots/1281884049597792277/vote)눌러주세요!", ephemeral=True)

@bot.slash_command(name="초대", description="루미나의 초대 사이트로 이동합니다.")
async def heart_command(interaction: nextcord.Interaction):
    await interaction.response.send_message("루미나를 서버를 초대하고 싶으면! [초대](https://discord.com/oauth2/authorize?client_id=1281884049597792277&permissions=8&integration_type=0&scope=bot)눌러주세요!", ephemeral=True)

    
@tasks.loop(minutes=60)
async def status_check():
    channel = bot.get_channel(1279413694178000920)
    if channel:
        await channel.send("봇은 현재 정상적으로 작동합니다.")
    
# 봇 시작 시간 기록
start_time = time.time()

# 로그 저장
command_logs = []

# 명령어 사용 시 로그 기록
@bot.listen("on_application_command")
async def log_command(interaction: nextcord.Interaction):
    command_logs.append(f"{interaction.user} used {interaction.command.name} at {time.ctime()}")
    if len(command_logs) > 10:  # 로그 최대 10개 유지
        command_logs.pop(0)

# 개발자 전용 명령어
@bot.slash_command(name="개발자전용", description="개발자 전용 관리 기능")
async def developer(interaction: nextcord.Interaction):
    # 개발자만 사용 가능하도록 권한 체크
    if interaction.user.id != 1091915995406413934:
        await interaction.response.send_message("이 명령어는 개발자 전용입니다.", ephemeral=False)
        return

    # 버튼 생성
    check_servers_button = Button(label="서버 확인", style=ButtonStyle.primary)
    restart_button = Button(label="재시작", style=ButtonStyle.danger)
    shutdown_button = Button(label="종료", style=ButtonStyle.danger)
    status_button = Button(label="상태 확인", style=ButtonStyle.primary)
    log_button = Button(label="로그 확인", style=ButtonStyle.secondary)
    api_test_button = Button(label="API 요청 테스트", style=ButtonStyle.danger)

    # 버튼 콜백 정의
    async def check_servers_callback(interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="봇이 참여 중인 서버 목록", color=0x00ff00)
        for guild in bot.guilds:
            embed.add_field(name=guild.name, value=f"ID: {guild.id}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def restart_callback(interaction: nextcord.Interaction):
        await interaction.response.send_message("봇을 재시작합니다...", ephemeral=True)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    async def shutdown_callback(interaction: nextcord.Interaction):
        await interaction.response.send_message("봇을 종료합니다...", ephemeral=True)
        await bot.close()  # 봇 종료

    async def status_callback(interaction: nextcord.Interaction):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        ping = round(bot.latency * 1000)
        
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{hours}시간 {minutes}분 {seconds}초"
        
        embed = nextcord.Embed(title="봇 상태 모니터링", color=0x3498db)
        embed.add_field(name="CPU 사용량", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="메모리 사용량", value=f"{memory_usage}%", inline=True)
        embed.add_field(name="응답 속도 (핑)", value=f"{ping}ms", inline=True)
        embed.add_field(name="업타임", value=uptime, inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def log_callback(interaction: nextcord.Interaction):
        log_text = "\n".join(command_logs) if command_logs else "로그가 없습니다."
        
        embed = nextcord.Embed(title="최근 명령어 사용 로그", description=log_text, color=0x3498db)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def api_test_callback(interaction: nextcord.Interaction):
        api_url = "https://api.publicapis.org/entries"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    api_response = data["entries"][0]["API"]
                    await interaction.response.send_message(f"API 요청 성공: {api_response}", ephemeral=True)
                else:
                    await interaction.response.send_message("API 요청 실패", ephemeral=True)

    # 콜백 등록
    check_servers_button.callback = check_servers_callback
    restart_button.callback = restart_callback
    shutdown_button.callback = shutdown_callback
    status_button.callback = status_callback
    log_button.callback = log_callback
    api_test_button.callback = api_test_callback

    # 버튼 뷰에 추가
    view = View()
    view.add_item(check_servers_button)
    view.add_item(restart_button)
    view.add_item(shutdown_button)
    view.add_item(status_button)
    view.add_item(log_button)
    view.add_item(api_test_button)

    # 메시지 전송
    await interaction.response.send_message("개발자 전용 관리 기능", view=view, ephemeral=True)

# 뉴스 API 키
# 퀴즈 데이터 (질문: 정답)
trivia_questions = {
    "태양계에서 가장 큰 행성은 무엇인가요?": "목성",
    "한국의 수도는 어디인가요?": "서울",
    "지구의 대기에서 가장 많은 기체는 무엇인가요?": "질소",
    "인간의 몸에서 가장 큰 장기는 무엇인가요?": "간",
    "물의 화학식은 무엇인가요?": "H2O",
}

@bot.slash_command(name="trivia", description="간단한 퀴즈 게임을 시작합니다.")
async def trivia(interaction: nextcord.Interaction):
    question, answer = random.choice(list(trivia_questions.items()))
    
    await interaction.response.send_message(f"퀴즈: {question}", ephemeral=True)
    
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await interaction.channel.send("시간이 초과되었습니다! 다음에 다시 시도해 주세요.")
    else:
        if msg.content.lower() == answer.lower():
            await interaction.channel.send("정답입니다! 🎉")
        else:
            await interaction.channel.send(f"틀렸습니다! 정답은 `{answer}`입니다.")

            
# 봇 실행
bot.run('bot')
