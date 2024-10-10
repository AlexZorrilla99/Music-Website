import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request

app= Flask(__name__)
client_id ='15325d7bf10241659c6fa8283e08b046'
client_secret ='fd0ea3b532ea4910b12f314b257349a5'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_tracks_by_genre(genre, limit=21):
    # Perform a search query with the specified genre
    results = sp.search(q=f'genre:"{genre}"', type='track', limit=15) #searches for tracks in genre
    tracks = results['tracks']['items']
    top_tracks = []

    for track in tracks:
        track_info = {
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'url': track['external_urls']['spotify'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
        top_tracks.append(track_info)
    
    return top_tracks

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genre = request.form['genre']
        try:
            tracks = get_top_tracks_by_genre(genre)
            if not tracks:
                error_message = "No tracks found for this genre."
                return render_template('index.html', error=error_message)
            return render_template('index.html', tracks=tracks, genre=genre)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render_template('index.html', error=error_message)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
