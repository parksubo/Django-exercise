from django.contrib import admin

from .models import Question, Choice

# admin 커스터마이징
# admin.TabularInline으로 변경하면 더 간략하게 볼 수도 있음
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # 선택지 3개까지 표시


# 필드 제목 필요없으면 오른쪽과 같이 작성도 가능#fields = ['pub_date', 'question_text']
# 필드가 여러개인 경우 양식을 아래와 같이 필드 세트로 분할 가능
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        #(제목, 내용)
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # 인라인에 ChoiceInline 클래스를 추가함으로써 question에서도 choice 수정 가능하도록 변경
    inlines = [ChoiceInline] 
    # question 리스트에 pub_date와 was_published_recently가 모두 보이게 변경
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # 날짜 정렬 필터 추가
    list_filter = ['pub_date']
    # 검색상자 추가
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
