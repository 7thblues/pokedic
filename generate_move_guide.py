import html, json, re
from pathlib import Path
ROOT = Path('/Users/beomsuk/pokemon/pokeruby')
OUT = Path('/Users/beomsuk/pokemon/ruby-sapphire-notes/ruby-sapphire-move-guide.html')

def read(rel): return (ROOT / rel).read_text(errors='ignore')
def clean_name(s): return s.replace('$$$$$$','').replace('$','').strip()
def title_from_const(s): return s.replace('_',' ').title().replace('Tm','TM').replace('Hm','HM')

FLAG_LABELS = {
    'F_AFFECTED_BY_KINGS_ROCK': '부가효과: 왕의징표석',
    'F_AFFECTED_BY_PROTECT': '방어 적용',
    'F_MIRROR_MOVE_COMPATIBLE': '따라하기 가능',
    'F_MAKES_CONTACT': '접촉기',
    'F_AFFECTED_BY_MAGIC_COAT': '매직코트 반사',
    'F_AFFECTED_BY_SNATCH': '가로챔 가능',
    'F_AFFECTED_BY_BRIGHT_POWDER': '반짝가루 영향',
}

def flag_label(flag):
    return FLAG_LABELS.get(flag, flag.replace('F_', '').replace('_', ' ').title())

moves_h = read('include/constants/moves.h')
move_ids = {m.group(1): int(m.group(2)) for m in re.finditer(r'#define\s+(MOVE_[A-Z0-9_]+)\s+(\d+)', moves_h)}
move_by_id = {v:k for k,v in move_ids.items()}

species_h = read('include/constants/species.h')
species_ids = {m.group(1): int(m.group(2)) for m in re.finditer(r'#define\s+(SPECIES_[A-Z0-9_]+)\s+(\d+)', species_h)}
species_by_id = {v:k for k,v in species_ids.items()}
hoenn_no = {}
for m in re.finditer(r'#define\s+HOENN_DEX_([A-Z0-9_]+)\s+(\d+)', species_h):
    hoenn_no['SPECIES_' + m.group(1)] = int(m.group(2))


MOVE_KO = {
    'MOVE_POUND':'막치기', 'MOVE_KARATE_CHOP':'태권당수', 'MOVE_DOUBLE_SLAP':'연속뺨치기', 'MOVE_COMET_PUNCH':'연속펀치', 'MOVE_MEGA_PUNCH':'메가톤펀치',
    'MOVE_PAY_DAY':'고양이돈받기', 'MOVE_FIRE_PUNCH':'불꽃펀치', 'MOVE_ICE_PUNCH':'냉동펀치', 'MOVE_THUNDER_PUNCH':'번개펀치', 'MOVE_SCRATCH':'할퀴기',
    'MOVE_VICE_GRIP':'찝기', 'MOVE_GUILLOTINE':'가위자르기', 'MOVE_RAZOR_WIND':'칼바람', 'MOVE_SWORDS_DANCE':'칼춤', 'MOVE_CUT':'풀베기',
    'MOVE_GUST':'바람일으키기', 'MOVE_WING_ATTACK':'날개치기', 'MOVE_WHIRLWIND':'날려버리기', 'MOVE_FLY':'공중날기', 'MOVE_BIND':'조이기',
    'MOVE_SLAM':'힘껏치기', 'MOVE_VINE_WHIP':'덩굴채찍', 'MOVE_STOMP':'짓밟기', 'MOVE_DOUBLE_KICK':'두번차기', 'MOVE_MEGA_KICK':'메가톤킥',
    'MOVE_JUMP_KICK':'점프킥', 'MOVE_ROLLING_KICK':'돌려차기', 'MOVE_SAND_ATTACK':'모래뿌리기', 'MOVE_HEADBUTT':'박치기', 'MOVE_HORN_ATTACK':'뿔찌르기',
    'MOVE_FURY_ATTACK':'마구찌르기', 'MOVE_HORN_DRILL':'뿔드릴', 'MOVE_TACKLE':'몸통박치기', 'MOVE_BODY_SLAM':'누르기', 'MOVE_WRAP':'김밥말이',
    'MOVE_TAKE_DOWN':'돌진', 'MOVE_THRASH':'난동부리기', 'MOVE_DOUBLE_EDGE':'이판사판태클', 'MOVE_TAIL_WHIP':'꼬리흔들기', 'MOVE_POISON_STING':'독침',
    'MOVE_TWINEEDLE':'더블니들', 'MOVE_PIN_MISSILE':'바늘미사일', 'MOVE_LEER':'째려보기', 'MOVE_BITE':'물기', 'MOVE_GROWL':'울음소리',
    'MOVE_ROAR':'울부짖기', 'MOVE_SING':'노래하기', 'MOVE_SUPERSONIC':'초음파', 'MOVE_SONIC_BOOM':'소닉붐', 'MOVE_DISABLE':'사슬묶기',
    'MOVE_ACID':'용해액', 'MOVE_EMBER':'불꽃세례', 'MOVE_FLAMETHROWER':'화염방사', 'MOVE_MIST':'흰안개', 'MOVE_WATER_GUN':'물대포',
    'MOVE_HYDRO_PUMP':'하이드로펌프', 'MOVE_SURF':'파도타기', 'MOVE_ICE_BEAM':'냉동빔', 'MOVE_BLIZZARD':'눈보라', 'MOVE_PSYBEAM':'환상빔',
    'MOVE_BUBBLE_BEAM':'거품광선', 'MOVE_AURORA_BEAM':'오로라빔', 'MOVE_HYPER_BEAM':'파괴광선', 'MOVE_PECK':'쪼기', 'MOVE_DRILL_PECK':'회전부리',
    'MOVE_SUBMISSION':'지옥의바퀴', 'MOVE_LOW_KICK':'안다리걸기', 'MOVE_COUNTER':'카운터', 'MOVE_SEISMIC_TOSS':'지구던지기', 'MOVE_STRENGTH':'괴력',
    'MOVE_ABSORB':'흡수', 'MOVE_MEGA_DRAIN':'메가드레인', 'MOVE_LEECH_SEED':'씨뿌리기', 'MOVE_GROWTH':'성장', 'MOVE_RAZOR_LEAF':'잎날가르기',
    'MOVE_SOLAR_BEAM':'솔라빔', 'MOVE_POISON_POWDER':'독가루', 'MOVE_STUN_SPORE':'저리가루', 'MOVE_SLEEP_POWDER':'수면가루', 'MOVE_PETAL_DANCE':'꽃잎댄스',
    'MOVE_STRING_SHOT':'실뿜기', 'MOVE_DRAGON_RAGE':'용의분노', 'MOVE_FIRE_SPIN':'회오리불꽃', 'MOVE_THUNDER_SHOCK':'전기쇼크', 'MOVE_THUNDERBOLT':'10만볼트',
    'MOVE_THUNDER_WAVE':'전기자석파', 'MOVE_THUNDER':'번개', 'MOVE_ROCK_THROW':'돌떨구기', 'MOVE_EARTHQUAKE':'지진', 'MOVE_FISSURE':'땅가르기',
    'MOVE_DIG':'구멍파기', 'MOVE_TOXIC':'맹독', 'MOVE_CONFUSION':'염동력', 'MOVE_PSYCHIC':'사이코키네시스', 'MOVE_HYPNOSIS':'최면술',
    'MOVE_MEDITATE':'요가포즈', 'MOVE_AGILITY':'고속이동', 'MOVE_QUICK_ATTACK':'전광석화', 'MOVE_RAGE':'분노', 'MOVE_TELEPORT':'순간이동',
    'MOVE_NIGHT_SHADE':'나이트헤드', 'MOVE_MIMIC':'흉내내기', 'MOVE_SCREECH':'싫은소리', 'MOVE_DOUBLE_TEAM':'그림자분신', 'MOVE_RECOVER':'HP회복',
    'MOVE_HARDEN':'단단해지기', 'MOVE_MINIMIZE':'작아지기', 'MOVE_SMOKESCREEN':'연막', 'MOVE_CONFUSE_RAY':'이상한빛', 'MOVE_WITHDRAW':'껍질에숨기',
    'MOVE_DEFENSE_CURL':'웅크리기', 'MOVE_BARRIER':'배리어', 'MOVE_LIGHT_SCREEN':'빛의장막', 'MOVE_HAZE':'흑안개', 'MOVE_REFLECT':'리플렉터',
    'MOVE_FOCUS_ENERGY':'기충전', 'MOVE_BIDE':'참기', 'MOVE_METRONOME':'손가락흔들기', 'MOVE_MIRROR_MOVE':'따라하기', 'MOVE_SELF_DESTRUCT':'자폭',
    'MOVE_EGG_BOMB':'알폭탄', 'MOVE_LICK':'핥기', 'MOVE_SMOG':'스모그', 'MOVE_SLUDGE':'오물공격', 'MOVE_BONE_CLUB':'뼈다귀치기',
    'MOVE_FIRE_BLAST':'불대문자', 'MOVE_WATERFALL':'폭포오르기', 'MOVE_CLAMP':'껍질끼우기', 'MOVE_SWIFT':'스피드스타', 'MOVE_SKULL_BASH':'로켓박치기',
    'MOVE_SPIKE_CANNON':'가시대포', 'MOVE_CONSTRICT':'휘감기', 'MOVE_AMNESIA':'망각술', 'MOVE_KINESIS':'숟가락휘기', 'MOVE_SOFT_BOILED':'알낳기',
    'MOVE_HI_JUMP_KICK':'무릎차기', 'MOVE_GLARE':'뱀눈초리', 'MOVE_DREAM_EATER':'꿈먹기', 'MOVE_POISON_GAS':'독가스', 'MOVE_BARRAGE':'구슬던지기',
    'MOVE_LEECH_LIFE':'흡혈', 'MOVE_LOVELY_KISS':'악마의키스', 'MOVE_SKY_ATTACK':'불새', 'MOVE_TRANSFORM':'변신', 'MOVE_BUBBLE':'거품',
    'MOVE_DIZZY_PUNCH':'잼잼펀치', 'MOVE_SPORE':'버섯포자', 'MOVE_FLASH':'플래시', 'MOVE_PSYWAVE':'사이코웨이브', 'MOVE_SPLASH':'튀어오르기',
    'MOVE_ACID_ARMOR':'녹기', 'MOVE_CRABHAMMER':'찝게햄머', 'MOVE_EXPLOSION':'대폭발', 'MOVE_FURY_SWIPES':'마구할퀴기', 'MOVE_BONEMERANG':'뼈다귀부메랑',
    'MOVE_REST':'잠자기', 'MOVE_ROCK_SLIDE':'스톤샤워', 'MOVE_HYPER_FANG':'필살앞니', 'MOVE_SHARPEN':'각지기', 'MOVE_CONVERSION':'텍스처',
    'MOVE_TRI_ATTACK':'트라이어택', 'MOVE_SUPER_FANG':'분노의앞니', 'MOVE_SLASH':'베어가르기', 'MOVE_SUBSTITUTE':'대타출동', 'MOVE_STRUGGLE':'발버둥',
    'MOVE_SKETCH':'스케치', 'MOVE_TRIPLE_KICK':'트리플킥', 'MOVE_THIEF':'도둑질', 'MOVE_SPIDER_WEB':'거미집', 'MOVE_MIND_READER':'마음의눈',
    'MOVE_NIGHTMARE':'악몽', 'MOVE_FLAME_WHEEL':'화염자동차', 'MOVE_SNORE':'코골기', 'MOVE_CURSE':'저주', 'MOVE_FLAIL':'바둥바둥',
    'MOVE_CONVERSION_2':'텍스처2', 'MOVE_AEROBLAST':'에어로블라스트', 'MOVE_COTTON_SPORE':'목화포자', 'MOVE_REVERSAL':'기사회생', 'MOVE_SPITE':'원한',
    'MOVE_POWDER_SNOW':'눈싸라기', 'MOVE_PROTECT':'방어', 'MOVE_MACH_PUNCH':'마하펀치', 'MOVE_SCARY_FACE':'겁나는얼굴', 'MOVE_FAINT_ATTACK':'속여때리기',
    'MOVE_SWEET_KISS':'천사의키스', 'MOVE_BELLY_DRUM':'배북', 'MOVE_SLUDGE_BOMB':'오물폭탄', 'MOVE_MUD_SLAP':'진흙뿌리기', 'MOVE_OCTAZOOKA':'대포무노포',
    'MOVE_SPIKES':'압정뿌리기', 'MOVE_ZAP_CANNON':'전자포', 'MOVE_FORESIGHT':'꿰뚫어보기', 'MOVE_DESTINY_BOND':'길동무', 'MOVE_PERISH_SONG':'멸망의노래',
    'MOVE_ICY_WIND':'얼다바람', 'MOVE_DETECT':'판별', 'MOVE_BONE_RUSH':'본러시', 'MOVE_LOCK_ON':'록온', 'MOVE_OUTRAGE':'역린',
    'MOVE_SANDSTORM':'모래바람', 'MOVE_GIGA_DRAIN':'기가드레인', 'MOVE_ENDURE':'버티기', 'MOVE_CHARM':'애교부리기', 'MOVE_ROLLOUT':'구르기',
    'MOVE_FALSE_SWIPE':'칼등치기', 'MOVE_SWAGGER':'뽐내기', 'MOVE_MILK_DRINK':'우유마시기', 'MOVE_SPARK':'스파크', 'MOVE_FURY_CUTTER':'연속자르기',
    'MOVE_STEEL_WING':'강철날개', 'MOVE_MEAN_LOOK':'검은눈빛', 'MOVE_ATTRACT':'헤롱헤롱', 'MOVE_SLEEP_TALK':'잠꼬대', 'MOVE_HEAL_BELL':'치료방울',
    'MOVE_RETURN':'은혜갚기', 'MOVE_PRESENT':'프레젠트', 'MOVE_FRUSTRATION':'화풀이', 'MOVE_SAFEGUARD':'신비의부적', 'MOVE_PAIN_SPLIT':'아픔나누기',
    'MOVE_SACRED_FIRE':'성스러운불꽃', 'MOVE_MAGNITUDE':'매그니튜드', 'MOVE_DYNAMIC_PUNCH':'폭발펀치', 'MOVE_MEGAHORN':'메가혼', 'MOVE_DRAGON_BREATH':'용의숨결',
    'MOVE_BATON_PASS':'바톤터치', 'MOVE_ENCORE':'앵콜', 'MOVE_PURSUIT':'따라가때리기', 'MOVE_RAPID_SPIN':'고속스핀', 'MOVE_SWEET_SCENT':'달콤한향기',
    'MOVE_IRON_TAIL':'아이언테일', 'MOVE_METAL_CLAW':'메탈크로우', 'MOVE_VITAL_THROW':'받아던지기', 'MOVE_MORNING_SUN':'아침햇살', 'MOVE_SYNTHESIS':'광합성',
    'MOVE_MOONLIGHT':'달의불빛', 'MOVE_HIDDEN_POWER':'잠재파워', 'MOVE_CROSS_CHOP':'크로스촙', 'MOVE_TWISTER':'회오리', 'MOVE_RAIN_DANCE':'비바라기',
    'MOVE_SUNNY_DAY':'쾌청', 'MOVE_CRUNCH':'깨물어부수기', 'MOVE_MIRROR_COAT':'미러코트', 'MOVE_PSYCH_UP':'자기암시', 'MOVE_EXTREME_SPEED':'신속',
    'MOVE_ANCIENT_POWER':'원시의힘', 'MOVE_SHADOW_BALL':'섀도볼', 'MOVE_FUTURE_SIGHT':'미래예지', 'MOVE_ROCK_SMASH':'바위깨기', 'MOVE_WHIRLPOOL':'바다회오리',
    'MOVE_BEAT_UP':'집단구타', 'MOVE_FAKE_OUT':'속이다', 'MOVE_UPROAR':'소란피기', 'MOVE_STOCKPILE':'비축하기', 'MOVE_SPIT_UP':'토해내기',
    'MOVE_SWALLOW':'꿀꺽', 'MOVE_HEAT_WAVE':'열풍', 'MOVE_HAIL':'싸라기눈', 'MOVE_TORMENT':'트집', 'MOVE_FLATTER':'부추기기',
    'MOVE_WILL_O_WISP':'도깨비불', 'MOVE_MEMENTO':'추억의선물', 'MOVE_FACADE':'객기', 'MOVE_FOCUS_PUNCH':'힘껏펀치', 'MOVE_SMELLING_SALT':'정신차리기',
    'MOVE_FOLLOW_ME':'날따름', 'MOVE_NATURE_POWER':'자연의힘', 'MOVE_CHARGE':'충전', 'MOVE_TAUNT':'도발', 'MOVE_HELPING_HAND':'도우미',
    'MOVE_TRICK':'트릭', 'MOVE_ROLE_PLAY':'역할', 'MOVE_WISH':'희망사항', 'MOVE_ASSIST':'조수', 'MOVE_INGRAIN':'뿌리박기',
    'MOVE_SUPERPOWER':'엄청난힘', 'MOVE_MAGIC_COAT':'매직코트', 'MOVE_RECYCLE':'리사이클', 'MOVE_REVENGE':'리벤지', 'MOVE_BRICK_BREAK':'깨트리다',
    'MOVE_YAWN':'하품', 'MOVE_KNOCK_OFF':'탁쳐서떨구기', 'MOVE_ENDEAVOR':'죽기살기', 'MOVE_ERUPTION':'분화', 'MOVE_SKILL_SWAP':'스킬스웹',
    'MOVE_IMPRISON':'봉인', 'MOVE_REFRESH':'리프레쉬', 'MOVE_GRUDGE':'원념', 'MOVE_SNATCH':'가로챔', 'MOVE_SECRET_POWER':'비밀의힘',
    'MOVE_DIVE':'다이빙', 'MOVE_ARM_THRUST':'손바닥치기', 'MOVE_CAMOUFLAGE':'보호색', 'MOVE_TAIL_GLOW':'반딧불', 'MOVE_LUSTER_PURGE':'러스터퍼지',
    'MOVE_MIST_BALL':'미스트볼', 'MOVE_FEATHER_DANCE':'깃털댄스', 'MOVE_TEETER_DANCE':'흔들흔들댄스', 'MOVE_BLAZE_KICK':'브레이즈킥', 'MOVE_MUD_SPORT':'흙놀이',
    'MOVE_ICE_BALL':'아이스볼', 'MOVE_NEEDLE_ARM':'바늘팔', 'MOVE_SLACK_OFF':'태만함', 'MOVE_HYPER_VOICE':'하이퍼보이스', 'MOVE_POISON_FANG':'독엄니',
    'MOVE_CRUSH_CLAW':'브레이크클로', 'MOVE_BLAST_BURN':'블러스트번', 'MOVE_HYDRO_CANNON':'하이드로캐논', 'MOVE_METEOR_MASH':'코멧펀치', 'MOVE_ASTONISH':'놀래키기',
    'MOVE_WEATHER_BALL':'웨더볼', 'MOVE_AROMATHERAPY':'아로마테라피', 'MOVE_FAKE_TEARS':'거짓울음', 'MOVE_AIR_CUTTER':'에어컷터', 'MOVE_OVERHEAT':'오버히트',
    'MOVE_ODOR_SLEUTH':'냄새구별', 'MOVE_ROCK_TOMB':'암석봉인', 'MOVE_SILVER_WIND':'은빛바람', 'MOVE_METAL_SOUND':'금속음', 'MOVE_GRASS_WHISTLE':'풀피리',
    'MOVE_TICKLE':'간지르기', 'MOVE_COSMIC_POWER':'코스믹파워', 'MOVE_WATER_SPOUT':'해수스파우팅', 'MOVE_SIGNAL_BEAM':'시그널빔', 'MOVE_SHADOW_PUNCH':'섀도펀치',
    'MOVE_EXTRASENSORY':'신통력', 'MOVE_SKY_UPPERCUT':'스카이업퍼', 'MOVE_SAND_TOMB':'모래지옥', 'MOVE_SHEER_COLD':'절대영도', 'MOVE_MUDDY_WATER':'탁류',
    'MOVE_BULLET_SEED':'기관총', 'MOVE_AERIAL_ACE':'제비반환', 'MOVE_ICICLE_SPEAR':'고드름침', 'MOVE_IRON_DEFENSE':'철벽', 'MOVE_BLOCK':'블록',
    'MOVE_HOWL':'멀리짖기', 'MOVE_DRAGON_CLAW':'드래곤크루', 'MOVE_FRENZY_PLANT':'하드플랜트', 'MOVE_BULK_UP':'벌크업', 'MOVE_BOUNCE':'뛰어오르다',
    'MOVE_MUD_SHOT':'머드숏', 'MOVE_POISON_TAIL':'포이즌테일', 'MOVE_COVET':'탐내다', 'MOVE_VOLT_TACKLE':'볼트태클', 'MOVE_MAGICAL_LEAF':'매지컬리프',
    'MOVE_WATER_SPORT':'물놀이', 'MOVE_CALM_MIND':'명상', 'MOVE_LEAF_BLADE':'리프블레이드', 'MOVE_DRAGON_DANCE':'용의춤', 'MOVE_ROCK_BLAST':'락블레스트',
    'MOVE_SHOCK_WAVE':'전격파', 'MOVE_WATER_PULSE':'물의파동', 'MOVE_DOOM_DESIRE':'파멸의소원', 'MOVE_PSYCHO_BOOST':'사이코부스트'
}

move_names = {}
for m in re.finditer(r'\[(MOVE_[A-Z0-9_]+)\]\s*=\s*_\("([^"]*)"\)', read('src/data/text/move_names_en.h')):
    move_names[m.group(1)] = clean_name(m.group(2))
species_names = {}
for m in re.finditer(r'\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*_\("([^"]*)"\)', read('src/data/text/species_names_en.h')):
    species_names[m.group(1)] = clean_name(m.group(2))

SPECIES_KO = {}
notes_path = OUT.parent / 'hoenn-pokedex-checklist.html'
if notes_path.exists():
    notes_html = notes_path.read_text(errors='ignore')
    marker = 'const DEX = '
    if marker in notes_html:
        start = notes_html.index(marker) + len(marker)
        end = notes_html.index('];', start) + 1
        for entry in json.loads(notes_html[start:end]):
            SPECIES_KO[entry['name']] = entry.get('nameKo', '')

def parse_expr_value(v):
    v = v.strip().rstrip(',')
    return v

battle = {}
text = read('src/data/battle_moves.c')
for m in re.finditer(r'\[(MOVE_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n\s*\},', text, re.S):
    const, body = m.group(1), m.group(2)
    fields = dict(re.findall(r'\.(\w+)\s*=\s*([^,\n]+(?:\s*\|\s*[^,\n]+)*)\s*,', body))
    flags = [f.strip() for f in fields.get('flags','0').split('|') if f.strip() and f.strip() != '0']
    typ = fields.get('type','TYPE_NORMAL').replace('TYPE_','').strip()
    battle[const] = {
        'id': move_ids.get(const, 0), 'const': const, 'name': move_names.get(const, title_from_const(const[5:])), 'nameKo': MOVE_KO.get(const, ''),
        'type': typ, 'category': 'Status' if fields.get('power','0').strip() == '0' else ('Physical' if typ in {'NORMAL','FIGHTING','POISON','GROUND','FLYING','BUG','ROCK','GHOST','STEEL'} else 'Special'),
        'power': fields.get('power','0').strip(), 'accuracy': fields.get('accuracy','0').strip(), 'pp': fields.get('pp','0').strip(),
        'effect': fields.get('effect','').replace('EFFECT_','').strip(), 'chance': fields.get('secondaryEffectChance','0').strip(),
        'target': fields.get('target','').replace('TARGET_','').replace('MOVE_TARGET_','').strip(), 'priority': fields.get('priority','0').strip(),
        'flags': [flag_label(f) for f in flags], 'learners': [], 'obtain': []
    }

# Level-up learnsets via pointer table.
level_text = read('src/data/pokemon/level_up_learnsets.h')
learnset_defs = {}
for m in re.finditer(r'const u16 (g\w+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\n\};', level_text, re.S):
    learnset_defs[m.group(1)] = [(int(a), b) for a,b in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*(MOVE_[A-Z0-9_]+)\s*\)', m.group(2))]
pointers_body = re.search(r'const u16 \*gLevelUpLearnsets\[\]\s*=\s*\{(.*?)\n\};', read('src/data/pokemon/level_up_learnset_pointers.h'), re.S).group(1)
pointers = re.findall(r'(g\w+LevelUpLearnset)', pointers_body)

species = []
for sid in sorted(species_by_id):
    const = species_by_id[sid]
    if const in {'SPECIES_NONE','SPECIES_EGG'} or const.startswith('SPECIES_OLD_UNOWN_'): continue
    if sid <= 0 or sid >= species_ids.get('SPECIES_EGG', 9999): continue
    name = species_names.get(const, title_from_const(const[8:]))
    species.append({'id':sid,'const':const,'name':name, 'nameKo': SPECIES_KO.get(name, ''), 'hoenn': hoenn_no.get(const), 'moves': []})
species_by_const = {s['const']: s for s in species}
species_by_id2 = {s['id']: s for s in species}

def add_learner(move_const, species_const, method):
    mv = battle.get(move_const)
    sp = species_by_const.get(species_const)
    if not mv or not sp: return
    mv['learners'].append({'species': sp['name'], 'hoenn': sp['hoenn'], **method})
    sp['moves'].append({'move': mv['name'], 'moveKo': mv.get('nameKo',''), 'moveId': mv['id'], 'type': mv['type'], 'category': mv['category'], **method})

for sid, ptr in enumerate(pointers):
    sp_const = species_by_id.get(sid)
    if not sp_const or sp_const not in species_by_const: continue
    for lvl, mv in learnset_defs.get(ptr, []):
        add_learner(mv, sp_const, {'method':'레벨업', 'detail':'Lv.' + str(lvl)})

# TM/HM move mapping.
pm = read('src/party_menu.c')
arr = re.search(r'const u16 TMHMMoves\[\]\s*=\s*\{(.*?)\n\};', pm, re.S).group(1)
tmhm_moves = re.findall(r'(MOVE_[A-Z0-9_]+)', arr)
tmhm_labels = []
for i, mv in enumerate(tmhm_moves):
    tmhm_labels.append(('TM%02d' % (i + 1)) if i < 50 else ('HM%02d' % (i - 49)))

tmhm_text = read('src/data/pokemon/tmhm_learnsets.h')
for m in re.finditer(r'\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*TMHM_LEARNSET\((.*?)\),', tmhm_text, re.S):
    sp_const, body = m.group(1), m.group(2)
    for code in re.findall(r'TMHM\(([^)]+)\)', body):
        code = code.strip()
        idx = None
        if code.startswith('TM'):
            idx = int(code[2:4]) - 1
        elif code.startswith('HM'):
            idx = 50 + int(code[2:4]) - 1
        if idx is not None and 0 <= idx < len(tmhm_moves):
            add_learner(tmhm_moves[idx], sp_const, {'method':tmhm_labels[idx], 'detail':''})

# Egg moves.
egg_text = read('src/data/pokemon/egg_moves.h')
for m in re.finditer(r'egg_moves\(([A-Z0-9_]+),\s*(.*?)\)', egg_text, re.S):
    sp_const = 'SPECIES_' + m.group(1)
    for mv in re.findall(r'MOVE_[A-Z0-9_]+', m.group(2)):
        add_learner(mv, sp_const, {'method':'알 기술', 'detail':'교배'})

# TM/HM obtain methods from item scripts and map scripts.
item_to_move = {}
for i, mv in enumerate(tmhm_moves):
    label = tmhm_labels[i]
    suffix = mv.replace('MOVE_', '')
    # item constants use SOLARBEAM while move is SOLAR_BEAM in this repo.
    candidates = [suffix, suffix.replace('_','')]
    for suf in candidates:
        item_to_move[f'ITEM_{label}_{suf}'] = (mv, label)

def add_obtain(item, source, kind):
    if item not in item_to_move: return
    mv, label = item_to_move[item]
    if mv not in battle: return
    if label.startswith('HM'):
        kind = '비소모'
    text = f'{label}: {source}'
    entry = {'kind': kind, 'text': text}
    if entry not in battle[mv]['obtain']:
        battle[mv]['obtain'].append(entry)

# Item ball scripts: derive route/map from label before EventScript.
ibs = read('data/item_ball_scripts.inc')
current_label = ''
for line in ibs.splitlines():
    lm = re.match(r'([A-Za-z0-9_]+)_EventScript_', line)
    if lm: current_label = lm.group(1)
    im = re.search(r'finditem\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', line)
    if im: add_obtain(im.group(1), f'{current_label} 필드 아이템', '유한')

for path in (ROOT/'data/maps').glob('*/scripts.inc'):
    loc = path.parent.name
    map_script_text = path.read_text(errors='ignore')
    for line in map_script_text.splitlines():
        gm = re.search(r'giveitem\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', line)
        if gm: add_obtain(gm.group(1), f'{loc} NPC/이벤트', '유한')
        fm = re.search(r'finditem\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', line)
        if fm: add_obtain(fm.group(1), f'{loc} 필드 아이템', '유한')
        sm = re.search(r'\.2byte\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', line)
        if sm: add_obtain(sm.group(1), f'{loc} 상점 구매', '반복')
    for bm in re.finditer(r'[A-Za-z0-9_]+::.*?(?=\n[A-Za-z0-9_]+::|\Z)', map_script_text, re.S):
        block = bm.group(0)
        if 'removecoins' not in block:
            continue
        cm = re.search(r'removecoins\s+(\d+)', block)
        coin_text = f' ({cm.group(1)} 코인)' if cm else ''
        for item in re.findall(r'additem\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', block):
            add_obtain(item, f'{loc} 게임코너 교환{coin_text}', '반복')

for path in (ROOT/'data/scripts').glob('*.inc'):
    if path.name == 'debug.inc': continue
    label = path.stem
    for line in path.read_text(errors='ignore').splitlines():
        lm = re.match(r'([A-Za-z0-9_]+)_EventScript_', line)
        if lm: label = lm.group(1)
        gm = re.search(r'giveitem\s+(ITEM_(?:TM|HM)\d+_[A-Z0-9_]+)', line)
        if gm: add_obtain(gm.group(1), f'{label} NPC/이벤트', '유한')

moves = [battle[c] for c in sorted(battle, key=lambda c: battle[c]['id']) if c != 'MOVE_NONE']
# Sort nested lists for stable display.
for mv in moves:
    mv['learners'].sort(key=lambda x: ((x['hoenn'] is None), x['hoenn'] or 999, x['species'], x['method'], x['detail']))
    mv['obtain'].sort(key=lambda x: (x['kind'] != '반복', x['text']))
def species_move_sort_key(x):
    method = x['method']
    detail = x.get('detail', '')
    if method == '레벨업':
        m = re.search(r'Lv\.(\d+)', detail)
        return (0, int(m.group(1)) if m else 999, x['move'])
    if method == '알 기술':
        return (1, 0, x['move'])
    if method.startswith('TM'):
        return (2, int(method[2:]) if method[2:].isdigit() else 999, x['move'])
    if method.startswith('HM'):
        return (3, int(method[2:]) if method[2:].isdigit() else 999, x['move'])
    return (9, 999, method, detail, x['move'])

for sp in species:
    sp['moves'].sort(key=species_move_sort_key)


for mv in moves:
    mv.pop('const', None)
for sp in species:
    sp.pop('const', None)
payload = {'moves': moves, 'species': sorted(species, key=lambda s: ((s['hoenn'] is None), s['hoenn'] or 999, s['id']))}
json_payload = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))

type_colors = {
'NORMAL':'#a8a878','FIRE':'#f08030','WATER':'#6890f0','ELECTRIC':'#f8d030','GRASS':'#78c850','ICE':'#98d8d8','FIGHTING':'#c03028','POISON':'#a040a0','GROUND':'#e0c068','FLYING':'#a890f0','PSYCHIC':'#f85888','BUG':'#a8b820','ROCK':'#b8a038','GHOST':'#705898','DRAGON':'#7038f8','DARK':'#705848','STEEL':'#b8b8d0'}
css_type = '\n'.join(f'.type-{k.lower()}, .type-chip.active.type-{k.lower()}{{background:{v};}}' for k,v in type_colors.items())
html_doc = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ruby/Sapphire Move Guide</title>
<style>
:root{{--ink:#1e211c;--muted:#687162;--line:#d7decd;--card:#fffef8;--leaf:#2f6f4e;--ruby:#b51f2a;--sapphire:#1d5eaa;}}
*{{box-sizing:border-box}} body{{margin:0;font:15px/1.45 -apple-system,BlinkMacSystemFont,'SF Pro Text','Apple SD Gothic Neo','Noto Sans KR','Helvetica Neue',sans-serif;color:var(--ink);background:radial-gradient(circle at 12% 0,#f6d4c4 0,transparent 28%),radial-gradient(circle at 90% 4%,#cfe4ff 0,transparent 30%),linear-gradient(135deg,#fffaf0,#edf5ed);-webkit-font-smoothing:antialiased}} main{{max-width:1440px;margin:0 auto;padding:32px 18px 72px}} h1{{margin:0;font-size:34px;letter-spacing:-.04em;font-weight:950}} p{{margin:7px 0 0;color:var(--muted)}} .hero{{display:flex;justify-content:space-between;gap:18px;align-items:end;margin-bottom:18px;padding:22px;border:1px solid var(--line);border-radius:24px;background:rgba(255,254,248,.88);box-shadow:0 18px 42px rgba(42,60,35,.1)}} .pill{{display:inline-flex;gap:6px;align-items:center;padding:6px 10px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--muted);font-weight:850}}
.toolbar{{display:grid;grid-template-columns:1.5fr repeat(4,minmax(130px,.55fr));gap:10px;padding:12px;margin:18px 0;border:1px solid var(--line);border-radius:20px;background:rgba(255,254,248,.94);box-shadow:0 16px 34px rgba(42,60,35,.08)}} input,select,button{{width:100%;border:1px solid var(--line);border-radius:13px;background:#fffefb;color:var(--ink);padding:10px 12px;font:inherit}} button{{cursor:pointer;font-weight:850}} .view-tabs,.type-row{{grid-column:1/-1;display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .label{{font-size:12px;font-weight:950;color:var(--muted)}} .chip{{width:auto;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:900;color:var(--muted);background:#fffefb}} .chip.active{{background:var(--leaf);border-color:var(--leaf);color:white}} .type-chip{{color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.35);border:0}} .type-chip.active{{color:#fff;box-shadow:0 0 0 3px rgba(42,60,35,.18), inset 0 0 0 2px rgba(255,255,255,.7);transform:translateY(-1px)}} {css_type}
.table-wrap{{overflow:auto;max-height:calc(100vh - 286px);border:1px solid var(--line);border-radius:18px;background:rgba(255,254,248,.96);box-shadow:0 18px 38px rgba(42,60,35,.08)}} .empty-state{{padding:34px;text-align:center;background:#fffef8;color:var(--muted)}} .empty-state strong{{display:block;margin-bottom:6px;color:var(--ink);font-size:18px;letter-spacing:-.02em}} .empty-state a{{display:inline-flex;margin-top:12px;padding:8px 12px;border-radius:999px;background:var(--leaf);color:white;text-decoration:none;font-weight:900}} table{{width:100%;min-width:1720px;border-collapse:separate;border-spacing:0}} body[data-view="pokemon"] table{{min-width:1120px}} body[data-view="pokemon"] .pokemon-cell{{width:150px;min-width:140px;max-width:170px}} body[data-view="pokemon"] .learn-table th:first-child,body[data-view="pokemon"] .learn-table td:first-child{{width:58px;white-space:nowrap;color:var(--muted);font-size:11px}} body[data-view="pokemon"] .learn-table th:last-child,body[data-view="pokemon"] .learn-table td:last-child{{width:58px;text-align:right}} body[data-view="pokemon"] .learn-table .type{{width:54px;min-width:54px;padding:2px 6px;font-size:10px}} body[data-view="pokemon"] .learn-table th,body[data-view="pokemon"] .learn-table td{{padding:5px 6px}} body[data-view="pokemon"] .learn-box{{min-width:0}} th{{position:sticky;top:0;z-index:5;text-align:left;font-size:12px;color:var(--muted);background:#eef4e7;padding:10px;border-bottom:1px solid var(--line)}} th.sortable{{cursor:pointer;user-select:none;white-space:nowrap}} th.sortable::after{{content:'↕';margin-left:6px;color:#9aa691;font-size:10px}} th.sortable.sorted-asc::after{{content:'↑';color:var(--leaf)}} th.sortable.sorted-desc::after{{content:'↓';color:var(--leaf)}} td{{padding:10px;border-bottom:1px solid var(--line);background:rgba(255,254,248,.95);vertical-align:top}} tr:hover td{{background:#f7fbef}} .name{{font-weight:950;letter-spacing:-.01em}} .type{{display:inline-flex;align-items:center;justify-content:center;width:74px;min-width:74px;padding:3px 8px;border-radius:999px;color:#fff;font-size:12px;font-weight:950;text-shadow:0 1px 0 rgba(0,0,0,.35)}} .type.physical{{border-radius:999px;box-shadow:inset 0 -2px 0 rgba(0,0,0,.22)}} .type.special{{border-radius:6px;box-shadow:inset 0 0 0 2px rgba(255,255,255,.42)}} .type.status{{border-radius:3px;background:repeating-linear-gradient(135deg,rgba(255,255,255,.22) 0 5px,rgba(0,0,0,.08) 5px 10px),#8b8d98;letter-spacing:.04em}} .cat{{display:inline-flex;padding:3px 8px;border-radius:999px;background:#f0f3ea;color:#44513f;font-size:12px;font-weight:900}} .cat.Physical{{background:#fff0e7;color:#a14b20}} .cat.Special{{background:#eaf2ff;color:#24558f}} .cat.Status{{background:#f0f0f4;color:#5a5b66}} .small{{color:var(--muted);font-size:12px}} .tags{{display:flex;gap:5px;flex-wrap:wrap}} .tag{{display:inline-flex;align-items:center;padding:3px 7px;border-radius:999px;background:#eef4e7;color:#40513a;font-size:12px;font-weight:850}} .tag.limited{{background:#fff0e8;color:#9a4d20}} .tag.repeat{{background:#e9f7ed;color:#2d7044}} .tag.nonconsume{{background:#eaf2ff;color:#24558f}} .learners{{max-width:430px}} .pokemon-list{{display:flex;gap:5px;flex-wrap:wrap;max-height:110px;overflow:auto}} .learn-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:start}} .learn-box{{min-width:360px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fffefb}} .learn-title{{padding:7px 9px;background:#eef4e7;color:#40513a;font-size:12px;font-weight:950}} .learn-table{{width:100%;min-width:0;border-collapse:collapse}} .learn-table th{{position:static;padding:6px 8px;background:#f7faef;font-size:11px}} .learn-table td{{padding:6px 8px;border-bottom:1px solid rgba(42,60,35,.1);font-size:12px;vertical-align:middle}} .learn-empty{{padding:10px;color:var(--muted);font-size:12px}} .move-title{{display:inline-grid;gap:1px;line-height:1.16;vertical-align:middle}} .move-ko{{display:block;color:var(--muted);font-size:11px;font-weight:800;letter-spacing:-.02em}} .move-link{{display:inline-flex;align-items:center;gap:7px;color:inherit;text-decoration:none;border-radius:12px;padding:2px 5px 2px 2px;margin:-2px 0;transition:background .14s ease,box-shadow .14s ease,transform .14s ease}} .move-link:hover{{text-decoration:none;background:#eef4e7;box-shadow:0 6px 16px rgba(47,111,78,.14);transform:translateY(-1px)}} .move-link:hover .type{{filter:saturate(1.12) brightness(1.04)}} .mon{{display:inline-flex;gap:4px;padding:3px 7px;border-radius:999px;background:#f3f6ef;color:#2f3b2b;font-size:12px;font-weight:800}} .method{{color:var(--muted)}} details{{max-width:460px}} summary{{cursor:pointer;font-weight:900;color:#2f513f}} .obtain-list{{display:grid;gap:4px;margin-top:6px}} .source-note{{font-size:12px;color:var(--muted)}} .note-nav{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 18px;padding:8px;border:1px solid var(--line);border-radius:999px;background:rgba(255,254,248,.82);box-shadow:0 10px 24px rgba(42,60,35,.08)}} .note-nav a{{display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:999px;color:var(--muted);text-decoration:none;font-size:13px;font-weight:900;transition:background .14s ease,color .14s ease,transform .14s ease}} .note-nav a:hover{{background:#eef4e7;color:var(--ink);transform:translateY(-1px)}} .note-nav a.active{{background:var(--leaf);color:white}} @media(max-width:900px){{.hero{{display:block}}.toolbar{{grid-template-columns:1fr 1fr}}main{{padding-inline:12px}}}}
</style></head><body><main><nav class="note-nav" aria-label="Ruby Sapphire notes"><a href="index.html">허브</a><a href="hoenn-pokedex-checklist.html">호연도감</a><a class="active" href="ruby-sapphire-move-guide.html">기술표</a></nav><section class="hero"><div><h1>기술 가이드</h1><p>Ruby/Sapphire Notes · pokeruby 저장소에서 추출한 기술표. 기술 검색과 도감에서 선택한 포켓몬의 습득 기술을 확인합니다.</p></div><div class="pill" id="count">0 shown</div></section>
<section class="toolbar"><input id="search" type="search" placeholder="기술명, 포켓몬명, 효과, 획득처 검색"><select id="category"><option value="">모든 분류</option><option>Physical</option><option>Special</option><option>Status</option></select><select id="power"><option value="">모든 위력</option><option value="status">변화기</option><option value="low">1-59</option><option value="mid">60-89</option><option value="high">90+</option></select><select id="method"><option value="">모든 습득법</option><option>레벨업</option><option>TM/HM</option><option>알 기술</option></select><select id="obtain"><option value="">TM/HM 획득 전체</option><option value="limited">유한 획득</option><option value="repeat">반복 구매</option><option value="nonconsume">비소모 HM</option></select><div class="view-tabs"><span class="label">보기</span><button class="chip active" type="button" data-view="moves">기술별</button><button class="chip" type="button" data-view="pokemon">포켓몬별</button></div><div class="type-row"><span class="label">타입</span><button class="chip active" type="button" data-type="">전체</button>{''.join('<button class="chip type-chip type-'+k.lower()+'" type="button" data-type="'+k+'">'+k+'</button>' for k in type_colors)}</div></section>
<div class="table-wrap"><table><thead id="thead"></thead><tbody id="body"></tbody></table></div><p class="source-note">출처: pokeruby `battle_moves.c`, `move_names_en.h`, `level_up_learnsets.h`, `tmhm_learnsets.h`, `egg_moves.h`, `party_menu.c`, `data/maps`, 게임코너 코인 교환, `data/item_ball_scripts.inc`.</p>
</main><script>const DATA={json_payload};
const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
let view='moves', type=''; let sortState={{moves:{{key:'id',dir:'asc'}},pokemon:{{key:'hoenn',dir:'asc'}}}}; const body=$('#body'), thead=$('#thead');
const typeBadge=(t,c='')=>'<span class="type type-'+t.toLowerCase()+(c?' '+c.toLowerCase():'')+'" title="'+esc(c||'type')+'">'+t+'</span>'; const catBadge=c=>'<span class="cat '+c+'">'+c+'</span>';
const methodOk=(row,m)=>!m||row.learners?.some(l=>m==='TM/HM'?/^TM|^HM/.test(l.method):l.method===m)||row.moves?.some(l=>m==='TM/HM'?/^TM|^HM/.test(l.method):l.method===m);
const methodLabel=x=>esc(x.method)+(!/^TM|^HM/.test(x.method)&&x.detail?' '+esc(x.detail):'');
const moveLabel=m=>'<span class="move-title"><span>'+esc(m.name)+'</span>'+(m.nameKo?'<span class="move-ko">'+esc(m.nameKo)+'</span>':'')+'</span>';
const powerOk=m=>{{const f=$('#power').value,p=Number(m.power);return !f||(f==='status'?p===0:f==='low'?p>0&&p<60:f==='mid'?p>=60&&p<90:p>=90)}};
const obtainOk=m=>{{const f=$('#obtain').value;return !f||(f==='limited'?m.obtain.some(o=>o.kind==='유한'):f==='repeat'?m.obtain.some(o=>o.kind==='반복'):m.obtain.some(o=>o.kind==='비소모'))}};
function naturalLearners(list){{return list.filter(l=>l.method==='레벨업'||l.method==='알 기술')}}
function learnerHtml(list){{const natural=naturalLearners(list);if(!natural.length)return '<span class="small">자력/교배 없음</span>';const shown=natural.slice(0,42).map(l=>'<span class="mon">'+esc(l.species)+(l.hoenn?' #'+l.hoenn:'')+' <span class="method">'+methodLabel(l)+'</span></span>').join('');return '<details open><summary>'+natural.length+'마리</summary><div class="pokemon-list">'+shown+(natural.length>42?'<span class="small">+'+(natural.length-42)+'</span>':'')+'</div></details>'}}
function obtainHtml(list){{if(!list.length)return '<span class="small">TM/HM 아님 또는 획득처 없음</span>';return '<div class="obtain-list">'+list.map(o=>'<span class="tag '+(o.kind==='반복'?'repeat':o.kind==='비소모'?'nonconsume':'limited')+'">'+esc(o.kind)+' · '+esc(o.text)+'</span>').join('')+'</div>'}}
function moveRow(m){{return '<tr id="move-'+esc(m.id)+'"><td><div class="name">'+moveLabel(m)+'</div></td><td>'+typeBadge(m.type,m.category)+'</td><td>'+esc(m.power==0?'--':m.power)+'</td><td>'+esc(m.accuracy==0?'--':m.accuracy)+'</td><td>'+esc(m.pp)+'</td><td><div class="name">'+esc(m.effect)+'</div><div class="small">우선도 '+esc(m.priority)+' · 확률 '+esc(m.chance)+' · '+esc(m.target)+'</div><div class="tags">'+m.flags.slice(0,5).map(f=>'<span class="tag">'+esc(f)+'</span>').join('')+'</div></td><td class="learners">'+learnerHtml(m.learners)+'</td><td>'+obtainHtml(m.obtain)+'</td></tr>'}}
const pokemonMoveLabel=m=>'<a class="move-link" href="#move-'+esc(m.moveId)+'" data-move-id="'+esc(m.moveId)+'">'+typeBadge(m.type,m.category)+'<span class="move-title"><span>'+esc(m.move)+'</span>'+(m.moveKo?'<span class="move-ko">'+esc(m.moveKo)+'</span>':'')+'</span></a>';
const learnMethodLabel=(m,mode)=>mode==='level'?(m.method==='레벨업'?esc(String(m.detail||'').replace('Lv.','')):m.method==='알 기술'?'알기술 교배':methodLabel(m)):esc(m.method);
const learnTable=(title, rows, mode)=>'<div class="learn-box"><div class="learn-title">'+title+' · '+rows.length+'</div>'+(rows.length?'<table class="learn-table"><thead><tr>'+(mode==='machine'?'<th>TM/HM</th><th>기술</th><th>타입</th>':'<th>Lv</th><th>기술</th><th>타입</th>')+'</tr></thead><tbody>'+rows.map(m=>'<tr><td>'+learnMethodLabel(m,mode)+'</td><td><span class="name">'+pokemonMoveLabel(m)+'</span></td><td>'+typeBadge(m.type,m.category)+'</td></tr>').join('')+'</tbody></table>':'<div class="learn-empty">없음</div>')+'</div>';
function pokemonRow(p){{const level=p.moves.filter(m=>!/^TM|^HM/.test(m.method)), machine=p.moves.filter(m=>/^TM|^HM/.test(m.method));return '<tr id="pokemon-'+p.id+'"><td class="pokemon-cell"><div class="name">'+esc(p.name)+(p.nameKo?' <span class="small">'+esc(p.nameKo)+'</span>':'')+'</div><div class="small">'+(p.hoenn?'Hoenn #'+p.hoenn:'National/extra')+'</div></td><td colspan="2"><div class="learn-grid">'+learnTable('레벨업/알 기술',level,'level')+learnTable('TM/HM',machine,'machine')+'</div></td></tr>'}}
const moveSortValue=(m,key)=>key==='name'?m.name:key==='type'?m.type:key==='category'?m.category:key==='power'||key==='accuracy'||key==='pp'||key==='learners'||key==='obtain'?Number(key==='learners'?naturalLearners(m.learners).length:key==='obtain'?m.obtain.length:m[key]):key==='effect'?m.effect:m.id;
const pokemonSortValue=(p,key)=>key==='name'?p.name:p.hoenn||9999;
function sortRows(rows, mode){{const state=sortState[mode], getter=mode==='moves'?moveSortValue:pokemonSortValue;return [...rows].sort((a,b)=>{{const av=getter(a,state.key), bv=getter(b,state.key);const cmp=typeof av==='number'&&typeof bv==='number'?av-bv:String(av).localeCompare(String(bv));return state.dir==='asc'?cmp:-cmp}})}}
const sortClass=(mode,key)=>sortState[mode].key===key?' sorted-'+sortState[mode].dir:'';
const th=(mode,key,label)=>'<th class="sortable'+sortClass(mode,key)+'" data-sort="'+key+'">'+label+'</th>';
function emptyPokemonState(){{thead.innerHTML='';body.innerHTML='<tr><td class="empty-state" colspan="3"><strong>도감에서 포켓몬을 선택하세요</strong><span>포켓몬별 기술표는 전체 나열하지 않고, 선택한 포켓몬의 기술만 표시합니다.</span><br><a href="hoenn-pokedex-checklist.html">호연도감으로 이동</a></td></tr>';$('#count').textContent='0 selected'}}
function render(){{document.body.dataset.view=view;const q=$('#search').value.trim().toLowerCase(), cat=$('#category').value, meth=$('#method').value;let rows=[]; if(view==='moves'){{thead.innerHTML='<tr>'+th('moves','name','기술')+th('moves','type','타입')+th('moves','power','위력')+th('moves','accuracy','명중')+th('moves','pp','PP')+th('moves','effect','효과/특성')+th('moves','learners','자력/교배 포켓몬')+th('moves','obtain','TM/HM 획득')+'</tr>'; rows=sortRows(DATA.moves.filter(m=>(!type||m.type===type)&&(!cat||m.category===cat)&&powerOk(m)&&methodOk(m,meth)&&obtainOk(m)&&(!q||JSON.stringify(m).toLowerCase().includes(q))),'moves'); body.innerHTML=rows.map(moveRow).join(''); $('#count').textContent=rows.length+' shown'}}else{{if(!q){{emptyPokemonState();return}}thead.innerHTML='<tr>'+th('pokemon','name','포켓몬')+'<th>레벨업/알 기술</th><th>TM/HM</th></tr>'; rows=sortRows(DATA.species.filter(p=>(!type||p.moves.some(m=>m.type===type))&&methodOk(p,meth)&&JSON.stringify(p).toLowerCase().includes(q)),'pokemon'); body.innerHTML=rows.length?rows.map(pokemonRow).join(''):'<tr><td class="empty-state" colspan="3"><strong>검색된 포켓몬이 없습니다</strong><span>도감에서 포켓몬 이름을 다시 선택하거나 검색어를 확인하세요.</span><br><a href="hoenn-pokedex-checklist.html">호연도감으로 이동</a></td></tr>'; $('#count').textContent=rows.length+' selected'}}}}
thead.addEventListener('click',e=>{{const cell=e.target.closest('th.sortable');if(!cell)return;const state=sortState[view], key=cell.dataset.sort;state.dir=state.key===key&&state.dir==='asc'?'desc':'asc';state.key=key;render()}});
function setView(nextView){{view=nextView;document.querySelectorAll('.view-tabs .chip').forEach(x=>x.classList.toggle('active',x.dataset.view===nextView))}}
function resetFilters(){{type='';for(const id of ['category','power','method','obtain']) $('#'+id).value='';document.querySelectorAll('.type-row .chip').forEach(x=>x.classList.toggle('active',x.dataset.type===''))}}
function focusMove(move){{setView('moves');resetFilters();$('#search').value=move.name;render();history.replaceState(null,'','#move-'+move.id);requestAnimationFrame(()=>document.getElementById('move-'+move.id)?.scrollIntoView({{block:'center'}}))}}
function focusPokemon(name){{const mon=DATA.species.find(p=>p.name.toLowerCase()===name.toLowerCase()||String(p.hoenn)===name);if(!mon)return false;setView('pokemon');resetFilters();$('#search').value=mon.name;render();history.replaceState(null,'','#pokemon-'+encodeURIComponent(mon.name));requestAnimationFrame(()=>document.getElementById('pokemon-'+mon.id)?.scrollIntoView({{block:'center'}}));return true}}
function applyInitialHash(){{const hash=decodeURIComponent(location.hash.slice(1));if(hash.startsWith('pokemon-')) focusPokemon(hash.slice('pokemon-'.length));else if(hash.startsWith('move-')){{const move=DATA.moves.find(m=>String(m.id)===hash.slice('move-'.length));if(move)focusMove(move)}}}}
body.addEventListener('click',e=>{{const link=e.target.closest('.move-link');if(!link)return;e.preventDefault();const move=DATA.moves.find(m=>String(m.id)===String(link.dataset.moveId));if(move)focusMove(move)}});
for(const id of ['search','category','power','method','obtain']) $('#'+id).addEventListener('input',render); document.querySelector('.view-tabs').addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;setView(b.dataset.view);render()}}); document.querySelector('.type-row').addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;type=b.dataset.type;document.querySelectorAll('.type-row .chip').forEach(x=>x.classList.toggle('active',x===b));render()}}); render(); applyInitialHash();</script></body></html>'''
OUT.write_text(html_doc)
print(OUT)
print(len(moves), 'moves', len(species), 'species')
