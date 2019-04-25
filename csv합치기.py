import pandas as pd

# csv 두개 병합
csv_poem = pd.read_csv("시.csv", encoding="utf-8")                       # 첫번째 csv 불러오기
csv_poem.drop(csv_poem.columns[[0,3]], axis=1, inplace = True)              # 1, 4번째 인덱스 삭제 (index, 시 본문)
csv_tag = pd.read_csv("tag.csv", encoding="utf-8")                       # 두번째 csv 불러오기
merged = csv_poem.merge(csv_tag, on = ('시 제목', '시인'), how='right')  # 두번째 csv 기준으로 병합
merged.to_csv("merged_csv.csv", index = True, encoding='utf-8')          # 최종 병합 후 csv 만들기
                                                                            # 인덱스 새로 만들기

print(merged)

