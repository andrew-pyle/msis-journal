---
layout: page
title: Papers List
permalink: /papers/
---

| Title | Author | Description | Date Read |
| ----- | ------ | ----------- | --------- | {% for paper in site.data.papers %}
| <a href="{{ paper.URL}}" target="_blank">{{ paper.Title }}</a> | {{paper.Author}} <br>| {{ paper.Description }} | {{ paper.Date }}|{% endfor %}
