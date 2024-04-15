import discord
import random
import pytz
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 음식 추천을 위한 리스트
food_list = [
    "짜장면",
    "짬뽕",
    "볶음밥",
    "피자",
    "햄버거",
    "초밥",
    "라면",
    "떡볶이",
    "치킨",
    "삼겹살",
    "족발",
    "햄버거",
    "샌드위치",
    "스테이크",
    "카레",
    "우동",
    "파스타",
    "냉면"
]

def recommend_food():
    return random.choice(food_list)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('안녕'):
        await message.channel.send('안녕하세요!!')

    if message.content.startswith('밥추천'):
        food = recommend_food()
        await message.channel.send(f'오늘은 {food} 어때요?')

    if message.content.startswith('음식추가'):
        new_food = message.content.split('음식추가 ')[1]
        food_list.append(new_food)
        # 추가된 음식을 추가한 사용자에게 알림
        await message.channel.send(f'{new_food} 음식이 추가되었습니다, {message.author.mention}님!')
        # 모든 채널에 공지
        for channel in message.guild.channels:
            await channel.send(f'새로운 음식 "{new_food}"이(가) 추가되었습니다! 오늘의 추천 메뉴에 포함될 수 있습니다.')

    if message.content.startswith('공지'):
        # 관리자 권한을 가진 사용자인지 확인
        if message.author.guild_permissions.administrator:
            # 공지 내용을 추출
            announcement = message.content.split('공지 ')[1]
            # 특정 채널 ID 지정
            target_channel_id = '특정 채널 ID'  # 여기에 채널 ID를 입력하세요
            # 특정 채널에 공지 발송
            target_channel = client.get_channel(int(target_channel_id))
            if target_channel:
                await target_channel.send(f'중요한 공지: {announcement}')
            else:
                await message.channel.send("유효하지 않은 채널 ID입니다.")
        else:
            await message.channel.send("관리자 권한이 필요합니다.")

    if message.content.startswith('한국시간'):
        korean_timezone = pytz.timezone('Asia/Seoul')
        korean_time = datetime.now(korean_timezone)
        formatted_time = korean_time.strftime('%Y-%m-%d %I:%M:%S %p')
        await message.channel.send(f'현재 한국 시간은 {formatted_time} 입니다.')

client.run('MTIyOTAzODI4MTA5MDQwMDMwNw.GN0e_Q.5kS9eguYeHqes9O772hy2WLHMDY-WjJVP21ry4')
