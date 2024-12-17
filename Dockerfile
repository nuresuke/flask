FROM python:3.12.7
WORKDIR /usr/src/app
RUN pip install flask==3.1.0
RUN pip install requests==2.32.3
RUN pip install blinker==1.9.0
RUN pip install certifi==2024.8.30
RUN pip install charset-normalizer==3.4.0
RUN pip install click==8.1.7
RUN pip install colorama==0.4.6
RUN pip install Flask==3.1.0
RUN pip install Flask-SQLAlchemy==3.1.1
RUN pip install greenlet==3.1.1
RUN pip install idna==3.10
RUN pip install itsdangerous==2.2.0
RUN pip install Jinja2==3.1.4
RUN pip install MarkupSafe==3.0.2
RUN pip install requests==2.32.3
RUN pip install SQLAlchemy==2.0.36
RUN pip install types-beautifulsoup4==4.12.0.20241020
RUN pip install types-html5lib==1.1.11.20241018
RUN pip install types-requests==2.32.0.20241016
RUN pip install typing_extensions==4.12.2
RUN pip install urllib3==2.2.3
RUN pip install Werkzeug==3.1.3

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]