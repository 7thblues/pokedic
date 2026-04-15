# pokeruby 분석 노트

이 문서는 다음 Codex/Claude 세션에서 `pokeruby` 분석을 빠르게 이어가기 위한 로컬 메모다.

기준 소스: `/Users/beomsuk/pokemon/pokeruby`  
공략/생성물 위치: `/Users/beomsuk/pokemon/ruby-sapphire-notes`

## 다음 세션 시작법

1. 이 파일과 `README.md`, `story-flow-ko.md`를 먼저 읽는다.
2. 공략 HTML을 수정해야 하면 `hoenn-pokedex-checklist.html`, `ruby-sapphire-move-guide.html`, `generate_move_guide.py`를 확인한다.
3. 원천 데이터가 의심되면 웹보다 `pokeruby` 소스를 먼저 본다.
4. 최종 HTML을 고친 뒤에는 가능하면 GitHub Pages 저장소에도 커밋/푸시한다.

## 현재 공략 문서

| 문서 | 목적 |
|---|---|
| `index.html` | 루비/사파이어 노트 허브 |
| `story-flow-ko.md` | 새 게임부터 엔딩 후처리까지 이벤트 흐름 |
| `ruby-sapphire-encounters.html` | 버전별 출현 차이, 쉬운 버전, 전용 포켓몬 |
| `hoenn-pokedex-checklist.html` | 호연도감 1-202 수집 체크리스트 |
| `ruby-sapphire-move-guide.html` | 기술/포켓몬별 기술 습득 공략 |
| `generate_move_guide.py` | 기술표 HTML 생성 스크립트 |
| `DEPLOY.md` | GitHub Pages 배포 절차 |

## pokeruby 주요 구조

| 영역 | 주요 파일 |
|---|---|
| 전투 메인 루프 | `src/battle_main.c`, `src/battle_script_commands.c`, `src/battle_util.c` |
| 전투 스크립트 | `data/battle_scripts_1.s`, `data/battle_scripts_2.s`, `include/macros/battle_script.inc` |
| 타입 상성 | `data/type_effectiveness.inc` |
| 기술 데이터 | `src/data/battle_moves.h`, `include/constants/moves.h`, `include/constants/battle_move_effects.h` |
| 포켓몬 기본 능력치 | `src/data/base_stats.h`, `include/constants/species.h` |
| 레벨업 기술 | `src/data/pokemon/level_up_learnsets.h` |
| TM/HM 습득 | `src/data/pokemon/tmhm_learnsets.h` |
| 진화/교배 관련 | `src/data/pokemon/evolution.h`, `src/pokemon_1.c`, `src/daycare.c` |
| 아이템 효과 | `src/item.c`, `src/item_use.c`, `src/pokemon_item_effect.c`, `src/data/items.h` |
| 야생 출현 | `src/data/wild_encounters.h`, `src/wild_encounter.c` |
| 맵 이벤트 | `data/maps/*/scripts.inc`, `data/scripts/*.inc`, `data/maps/*/map.json` |
| 플래그/변수 | `include/constants/flags.h`, `include/constants/vars.h`, `src/event_data.c` |
| 텍스트/표시명 | `src/data/text/*.h`, `data/text/*.inc`, `src/data/pokemon_graphics/*` |

## 전투 로직 요약

전투는 C 코드와 전투 전용 스크립트가 섞여 있다. 데미지 계산, 명중, 상태 이상, 능력치 랭크 변경, 아이템 처리 같은 핵심 처리는 `src/battle_script_commands.c`와 `src/battle_util.c`를 중심으로 추적한다. 전투 진행 자체는 `src/battle_main.c`와 각 컨트롤러 파일이 관리한다.

타입 상성은 `data/type_effectiveness.inc`의 3바이트 테이블이다. 값은 `20 = 2배`, `10 = 1배`, `5 = 0.5배`, `0 = 무효`로 해석한다. 이 테이블에 없는 조합은 기본 1배다. 복합 타입은 각 타입의 배율을 곱하므로 4배, 0.25배, 무효가 발생한다.

기술의 타입/위력/명중/효과는 `src/data/battle_moves.h`에 있다. Gen 3 기준 물리/특수 분류는 기술별이 아니라 타입 종속이다. 불꽃/물/전기/풀/얼음/에스퍼/드래곤/악은 특수, 노말/격투/독/땅/비행/벌레/바위/고스트/강철은 물리다. 변화기는 별도 상태 기술로 표시하면 된다.

능력치 버프/디버프는 전투 중 랭크가 `-6..+6` 범위로 움직인다. 검무, 울음소리, 방어 상승류는 전투 스크립트와 `EFFECT_*` 처리에서 연결된다. 추적 시작점은 `include/constants/battle_move_effects.h`, `src/data/battle_moves.h`, `src/battle_script_commands.c`다.

전투 중 아이템은 일반 아이템 사용과 배틀 아이템 계열을 구분해야 한다. 회복약/상태회복/기력의조각 등은 `src/pokemon_item_effect.c`와 `src/item_use.c`를 같이 본다. 일회성 전투 아이템은 사용 즉시 포켓몬 데이터, HP, 상태, 랭크 또는 휘발 상태에 반영되고 소모된다.

## 공략 데이터 추출 기준

도감 체크리스트는 포켓몬별로 다음 정보를 합쳐 만든다.

| 정보 | 원천 |
|---|---|
| 이름/내부 species | `include/constants/species.h`, 이름 테이블 |
| 한국어 이름 | 로컬 매핑 테이블, 기존 HTML 생성 데이터 |
| 타입 | `src/data/base_stats.h` |
| 기본 능력치 | `src/data/base_stats.h` |
| 진화 조건 | `src/data/pokemon/evolution.h` |
| 출현 장소/확률 | `src/data/wild_encounters.h` |
| 버전 차이 | Ruby/Sapphire 전용 출현 테이블 비교 |
| 스프라이트 | `graphics/pokemon/*`, `data/graphics/pokemon/*.inc` |
| 방어 상성 | `data/type_effectiveness.inc`와 포켓몬 타입 조합 |

기술 공략은 다음 정보를 합쳐 만든다.

| 정보 | 원천 |
|---|---|
| 기술명/내부 move | `include/constants/moves.h`, 이름 테이블 |
| 한국어 기술명 | 로컬 매핑 테이블 |
| 타입/위력/명중/PP/효과 | `src/data/battle_moves.h` |
| 레벨업 습득 | `src/data/pokemon/level_up_learnsets.h` |
| TM/HM 습득 | `src/data/pokemon/tmhm_learnsets.h` |
| 알 기술 | 관련 learnset 데이터와 교배 로직 |
| 기술 획득처 | 맵 스크립트, 아이템볼, 상점, 게임코너, HM 이벤트 |
| 유한/반복 가능 | TM은 대부분 유한, HM은 반복 가능, 상점/게임코너 판매는 반복 가능 |

## 이미 정리한 사용자 요구사항

- 내부 상수명은 최종 HTML에 그대로 노출하지 않는다.
- `SPECIES_*`, `MOVE_*`, `AFFECTED_BY_*`, `SELECTED_POKEMON` 같은 값은 자연어/한글 설명으로 변환한다.
- 타입 배지는 인게임 감성보다 웹 가독성을 우선하되, 타입별 색상은 일관되게 유지한다.
- 도감 체크는 Ruby/Sapphire 각각 별도로 저장한다.
- 체크 상태는 브라우저 `localStorage`에 저장한다.
- 도감 이름 클릭 시 해당 포켓몬의 기술 목록으로 이동한다.
- 기술명 클릭 시 기술별 상세/목록 위치로 이동한다.
- 포켓몬별 기술표에서는 레벨업/알 기술과 TM/HM 기술을 분리한다.
- 레벨업 기술은 레벨순으로 정렬한다.
- 기술명은 영문 1줄, 한글 2줄 형태로 컬럼 폭을 줄인다.
- 타입 배지는 기술명 앞에 둔다.
- 링크는 밑줄 기본 스타일 대신 hover 시 시각효과를 준다.
- 헤더/허브/현황 표시 스타일은 도감과 기술표가 같은 테마로 보여야 한다.
- 큰 히어로 셀은 제거하고 리스트/테이블 영역을 더 확보한다.

## 스토리 공략 흐름

상세 흐름은 `story-flow-ko.md`를 기준으로 한다. 핵심 순서는 다음과 같다.

1. 리틀루트 이사, 집 이벤트
2. 101번도로 털보박사 구조, 스타팅 선택
3. 연구소에서 스타팅 확정, 103번도로 라이벌전
4. 도감/몬스터볼 수령, 자유 진행 시작
5. 페탈버그 노먼/월리 포획 이벤트
6. 러스트보로 체육관, 데본 화물 회수
7. 무로마을, 스티븐 편지 전달
8. 잿빛 해양박물관, 데본 화물 전달
9. 보라시티와 굴뚝산/운석 사건
10. 용암마을 체육관, 사막 고글, 노먼전
11. 날씨 연구소, 캐스퐁, 공중날기
12. 120번도로 데본스코프, 검방울 체육관
13. 송화산 오브 사건, 잿빛 항구 잠수정 탈취
14. 해안시티 아지트, 해저동굴, 그란돈/가이오가 각성
15. 루네시티, 기원의 동굴, 8번째 배지
16. 챔피언로드, 사천왕, 스티븐전, 명예의 전당
17. 클리어 후 SS 티켓, 라티오스/라티아스 TV 이벤트, 후일담 요소 개방

## 이벤트 분석 시작점

| 구간 | 파일 |
|---|---|
| 새 게임 시작 | `data/scripts/new_game.inc`, `data/maps/InsideOfTruck/scripts.inc` |
| 리틀루트 초기 | `data/maps/LittlerootTown/scripts.inc` |
| 털보박사 구조 | `data/maps/Route101/scripts.inc` |
| 연구소/도감 | `data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc` |
| 첫 라이벌전 | `data/maps/Route103/scripts.inc` |
| 데본 이벤트 | `data/maps/RustboroCity/scripts.inc`, `data/maps/RustboroCity_DevonCorp_3F/scripts.inc` |
| 스티븐 편지 | `data/maps/GraniteCave_StevensRoom/scripts.inc` |
| 해양박물관 | `data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc` |
| 굴뚝산 | `data/scripts/magma_chimney.inc`, `data/scripts/magma_summit.inc` |
| 날씨 연구소 | `data/maps/Route119_WeatherInstitute_2F/scripts.inc` |
| 데본스코프 | `data/maps/Route120/scripts.inc` |
| 오브/전설 | `data/maps/SeafloorCavern_Room9/scripts.inc`, `data/scripts/cave_of_origin.inc` |
| 리그/엔딩 | `data/maps/EverGrandeCity_PokemonLeague/scripts.inc`, `data/maps/EverGrandeCity_ChampionsRoom/scripts.inc`, `data/maps/EverGrandeCity_HallOfFame/scripts.inc`, `data/scripts/hall_of_fame.inc` |

## 추가로 정리할 가치가 있는 문서

- `battle-logic-ko.md`: 전투 데미지, 명중, 랭크, 상태이상, 도구 효과를 코드 경로 중심으로 더 깊게 정리.
- `data-extraction-ko.md`: 도감/기술표 HTML을 재생성하기 위한 데이터 파이프라인 정리.
- `version-differences-ko.md`: Ruby/Sapphire 전용/쉬운 포켓몬 판정 규칙과 예외 정리.
- `deploy-history-ko.md`: GitHub Pages 배포 URL, 저장소, 커밋 절차 정리.

## 주의사항

- `pokeruby`는 원작 GBA 디컴파일 소스라 데이터가 C, asm, inc, json에 분산되어 있다.
- 같은 이름의 맵이라도 층/방이 나뉘므로 지도 표기는 연결 루트까지 확인해야 한다.
- 출현 장소가 `Underwater`, `Meteor Falls`처럼 넓게만 나오면 실제 접근 루트와 방 이름을 보강해야 한다.
- 버전 전용 포켓몬은 직접 출현뿐 아니라 진화 전 포켓몬의 버전 제한도 같이 반영해야 한다.
- `Ruby/Sapphire 공통`과 `특정 버전이 더 쉬움`은 중복 표기를 피하고, 전용/쉬움/공통을 일관된 스타일로 구분한다.
- 자료 출처가 `pokeruby` 안에 있으면 웹 검색보다 로컬 소스를 우선한다.
