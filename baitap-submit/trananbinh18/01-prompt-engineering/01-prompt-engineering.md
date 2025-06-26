- Prompt 1:
```
You're the excellent teacher, Known to be very good at creating responsible assignments for students, especially as multiple choice exercise.
I'm a teacher, help me make a multiple choice exercise test for my students.
The exercise should having `Input number of questions` questions, each question having 4 choices, mark the correct answer
The result follow the format:
"""
Question: [Question]
Choices:
[ ] [Option1]
[ ] [Option2]
[x] [CorrectOption]
[ ] [Option4]
"""
Exercise topic:
`Input Topic Here`
Focus on:
+ `Input Criticality 1`
+ `Input Criticality 2`
```


- Prompt 2
```
You are an excellent writer. Trịnh Công Sơn, Thích Nhất Hạnh, Xuân Diệu, and Vũ Trọng Phùng have greatly influenced your writing style.
Help me make a literary discussion about this paragraph then rewrite it with your flows.
Notes: maximum additional words is `Input number of words`, the answer must use the language of the paragraph, and it's even better if you focus on the style rather than mentioning those who influenced you.

Paragraph:
"""
`Input Here`
"""

```

- Prompt 3
```
I'm facebook page manager. 
Help me detect which comments are positive or negative. then analyze summary the result. The Summary should show assessment and Prediction show how people will react with the page's posts in the future.
finally rating it with score from 1 to 10 (1 is very negative and 10 is very positive).
e.g comments: 
+ "đăng bài như cái qq, mẹ nửa tiếng anh nửa tiếng việt. Nhìn là không muốn trả lời :)" - negative
+ "Đồ ăn nhìn rất là ngon,mong là may chi bạn đồ ăn tươi sạch,bán hàng bằng lương tâm <3 <3 <3" - positive
+ "bài viết rõ ràng đi vào ý chính, dễ hiểu dễ tiếp thu. 10 điểm" - positive
+ "1 đội tuyển lớn mạnh mà sao đi thuê Media  toàn lũ ô hợp , cơm hàng cháo chợ , nhìn dơ bẩn ko vậy trời 🙄🙄🙄🙄" - negative
+ "Nước súp trộn hơi mặn nha, ai ăn mặn mới ngon, cô này ko chửi khách với lại cô cũng vui tính, sẽ thông cảm cho cô." - positive
the output should follow the format:
===
+ "[comment 1]" - [positive/negative]
+ "[comment 2]" - [positive/negative]
- Positive: [Percent of number of negative over total]
- Negative: [Percent of number of positive over total]
- Summary: [Summary]
- Prediction: [Prediction]
- Score: [score/10]
===

"""
`Input Here`
"""
```


- Prompt 4
```
You are excellent senior engineer.
Help me finding bugs in code bellow. 
Exception/Stack trace:
===
`Input Here`
===
Code:
===
`Input Here`
===

The result should have
- Explain the purpose of the code
- Explain the current exception
- Make comments on state that you think it cause bugs
- Extra potential states you think it can cause bugs in future
- Suggested fixes Full code, put the comments to explains
```

- Prompt 5
```
You are the excellent tour guy.
I'm going to visit `Input place`, Help me best places to visit, good restaurants, fun amusement park, and so on
The result should include Summary section and Places section.
Summary section should overview about the place i'm going to visit,specialty, local foods.
Each place in places section should follow format:
'''
- Name:
- Location:
- Recommend level: [should try / must try]
- Hours if it have: 
- Overview: 
- Reference website links
'''
```

- Prompt 6
```
Help me to summary this article
The summary should list all characters had been mentioned if it relate to article's content.
summary the content make it easy to understand. the maximum content is 200 words

===
`Input here`
===

```