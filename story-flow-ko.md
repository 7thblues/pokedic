# Pokemon Ruby/Sapphire Story Flow

이 문서는 `pokeruby`의 이벤트 스크립트를 기준으로 정리한 루비/사파이어 메인 스토리 흐름이다.

## 전체 흐름

1. 이사 트럭에서 시작한다. 성별에 따라 브렌던/봄이 집 리스폰 위치와 초기 플래그가 갈린다.

2. 리틀루트에서 엄마를 따라 집에 들어가고, 집 이벤트 후 마을 상태가 진행된다.

3. 101번도로에서 털보박사 구조 이벤트가 발생하고, 스타팅 포켓몬을 고른다. 이후 `FLAG_RESCUED_BIRCH`, `VAR_BIRCH_LAB_STATE`, `VAR_ROUTE101_STATE`가 갱신된다.

4. 연구소에서 스타팅 포켓몬을 정식으로 받고, 103번도로의 라이벌전을 하러 가게 된다.

5. 103번도로에서 라이벌과 첫 전투를 한다. 승리 후 연구소 귀환 플래그가 열리고 `FLAG_DEFEATED_RIVAL_ROUTE103`이 세팅된다.

6. 연구소에서 포켓몬 도감과 몬스터볼을 받는다. 이때 `FLAG_ADVENTURE_STARTED`, `FLAG_SYS_POKEDEX_GET`, `VAR_ROUTE102_ACCESSIBLE`이 세팅되며 본격적인 자유 진행이 시작된다.

7. 페탈버그에서 아버지 노먼을 만나고, 월리가 포켓몬을 잡는 이벤트가 진행된다. 이후 러스트보로 방향으로 스토리가 열린다.

8. 러스트보로 체육관에서 첫 배지를 얻는다.

9. 러스트보로 이후 데본 직원/데본 화물 이벤트가 시작된다. 116번도로와 러스트터프 터널 쪽에서 화물을 되찾고, 러스트보로 데본 사장에게 안내된다.

10. 데본 코퍼레이션 3층에서 편지와 포켓내비를 받고, 스티븐에게 편지를 배달하는 목표가 생긴다. 브리니 항로 이벤트도 이때 열린다.

11. 무로마을/석영동굴에서 스티븐에게 편지를 전달하고 강철날개 TM을 받는다. 핵심 플래그는 `FLAG_DELIVERED_STEVEN_LETTER`다.

12. 잿빛도시 해양박물관에서 선장에게 데본 화물을 전달하려다 악의 조직 이벤트가 발생한다. 루비/사파이어에 따라 마그마단/아쿠아단 대사와 리더가 갈린다. 완료 후 `FLAG_DELIVERED_DEVON_GOODS`가 세팅된다.

13. 보라시티, 잿빛-보라 라이벌전, 전기 체육관 이후 북쪽으로 진행한다. 이후 운석/코스모 박사/유성폭포/굴뚝산 이벤트로 넘어간다.

14. 굴뚝산 이벤트에서 악의 조직을 물리치고 운석 사건을 해결한다. 여기서 `FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY`가 세팅되고, 용암마을 진행이 열린다.

15. 용암마을 체육관 후 고글을 받고 사막 진입이 가능해진다. 이후 페탈버그로 돌아가 노먼과 싸워 5번째 배지를 얻는다. 노먼 이후 월리 집에서 파도타기 HM을 받는 흐름으로 동쪽 진행이 열린다.

16. 119번도로 날씨 연구소에서 악의 조직을 몰아내고 캐스퐁을 받는다. `VAR_WEATHER_INSTITUTE_STATE`, `FLAG_HIDE_EVIL_TEAM_WEATHER_INSTITUTE`, `FLAG_RECEIVED_CASTFORM`이 갱신된다.

17. 119번도로 라이벌전 후 공중날기 HM을 받는다.

18. 120번도로에서 스티븐이 데본스코프를 주고, 켈리몬 이벤트를 통해 검방울시티 체육관 진행이 열린다.

19. 송화산에서 오브 사건이 발생하고, 이후 잿빛도시 항구 잠수정 탈취 이벤트로 이어진다. `VAR_SLATEPORT_STATE`, `VAR_SLATEPORT_HARBOR_STATE`, `FLAG_RECEIVED_RED_OR_BLUE_ORB` 등이 쓰인다.

20. 해안시티 아지트/잠수정 추적 이후 해저동굴로 들어가고, 그란돈/가이오가 각성 이벤트가 발생한다. 이때 전역 날씨 플래그와 루트128/루네시티 상태가 바뀐다.

21. 루네시티에서 스티븐과 윤진/월리스가 등장하고, 기원의 동굴 진입으로 전설 포켓몬 사건을 해결한다. 이후 루네 체육관이 열리고 8번째 배지를 얻는다.

22. 모든 배지를 얻으면 챔피언로드/포켓몬리그로 진행한다. 리그 입장 스크립트는 배지 플래그를 검사하고, 통과 시 `FLAG_ENTERED_ELITE_FOUR`를 세팅한다.

23. 사천왕 방은 `VAR_ELITE_4_STATE`와 각 사천왕 격파 플래그로 순서가 관리된다. 순서는 시드니, 회연, 미혜, 권수다.

24. 챔피언 방에서 스티븐과 전투한다. 승리 후 라이벌과 박사가 들어오고, 도감 평가 후 명예의 전당으로 이동한다.

25. 명예의 전당에서 파티 기록 연출을 실행하고, 클리어 후처리 플래그를 세팅한 뒤 `special GameClear`로 크레딧에 들어간다.

26. 클리어 후처리에서 사천왕 상태 초기화, SS 티켓 이벤트 준비, 라티오스/라티아스 TV 이벤트, 스티븐 집의 메탕/다이빙 HM 상태 등이 열린다.

## 주요 배지 플래그

- `FLAG_BADGE01_GET`: Rustboro Gym
- `FLAG_BADGE02_GET`: Dewford Gym
- `FLAG_BADGE03_GET`: Mauville Gym
- `FLAG_BADGE04_GET`: Lavaridge Gym
- `FLAG_BADGE05_GET`: Petalburg Gym
- `FLAG_BADGE06_GET`: Fortree Gym
- `FLAG_BADGE07_GET`: Mossdeep Gym
- `FLAG_BADGE08_GET`: Sootopolis Gym

## 주요 코드 위치

- `pokeruby/data/maps/InsideOfTruck/scripts.inc`: 새 게임 시작
- `pokeruby/data/maps/LittlerootTown/scripts.inc`: 리틀루트 초기 이벤트
- `pokeruby/data/maps/Route101/scripts.inc`: 털보박사 구조와 스타팅 선택
- `pokeruby/data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc`: 스타팅 확정, 도감, 모험 시작
- `pokeruby/data/maps/Route103/scripts.inc`: 첫 라이벌전
- `pokeruby/data/maps/RustboroCity/scripts.inc`: 데본 화물 반환
- `pokeruby/data/maps/RustboroCity_DevonCorp_3F/scripts.inc`: 편지와 포켓내비
- `pokeruby/data/maps/GraniteCave_StevensRoom/scripts.inc`: 스티븐 편지 전달
- `pokeruby/data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc`: 해양박물관 악의 조직 이벤트
- `pokeruby/data/scripts/magma_chimney.inc`: 굴뚝산 악의 조직 이벤트
- `pokeruby/data/maps/Route119_WeatherInstitute_2F/scripts.inc`: 날씨 연구소 이벤트
- `pokeruby/data/maps/Route120/scripts.inc`: 데본스코프와 켈리몬
- `pokeruby/data/maps/SeafloorCavern_Room9/scripts.inc`: 전설 포켓몬 각성
- `pokeruby/data/maps/EverGrandeCity_PokemonLeague/scripts.inc`: 리그 입장
- `pokeruby/data/maps/EverGrandeCity_ChampionsRoom/scripts.inc`: 챔피언전
- `pokeruby/data/maps/EverGrandeCity_HallOfFame/scripts.inc`: 명예의 전당과 게임 클리어
- `pokeruby/data/scripts/hall_of_fame.inc`: 클리어 후처리
