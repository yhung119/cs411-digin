# cat create_db.sql | python manage.py dbshell
cat create_user.sql | python manage.py dbshell
cat create_token.sql | python manage.py dbshell
cat create_polls.sql | python manage.py dbshell

python manage.py makemigrations
python manage.py migrate sessions

pip install mysql-connector-python-rf
pip install -U googlemaps
pip install git+https://github.com/boudinfl/pke.git

python -m nltk.downloader stopwords
python -m nltk.downloader universal_tagset
python -m spacy download en # download the english model


pip install wordcloud
pip install matplotlib