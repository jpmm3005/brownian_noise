const redirectUri = "https://jpmm3005.github.io/brownian_noise/";
const scopes = "user-top-read user-read-private";

function generateRandomString(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    return Array.from(crypto.getRandomValues(new Uint8Array(length)))
            .map(x => chars[x % chars.length])
            .join('');
}

async function generateCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

  async function redirectToSpotify() {
    const clientId = document.getElementById("clientIdInput").value.trim();

    if (!clientId) {
      document.getElementById("message").innerText = "Please enter a valid Client ID.";
      return;
    }

    localStorage.setItem("client_id", clientId);

    const codeVerifier = generateRandomString(128);
    const codeChallenge = await generateCodeChallenge(codeVerifier);
    localStorage.setItem('code_verifier', codeVerifier);

    const params = new URLSearchParams({
      response_type: 'code',
      client_id: clientId,
      scope: scopes,
      redirect_uri: redirectUri,
      code_challenge_method: 'S256',
      code_challenge: codeChallenge
    });

    window.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
  }

  async function getAccessToken(code) {
    const codeVerifier = localStorage.getItem('code_verifier');
    const clientId = localStorage.getItem('client_id');

    const body = new URLSearchParams({
      client_id: clientId,
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: redirectUri,
      code_verifier: codeVerifier
    });

    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body
    });

    return await response.json();
  }

  async function getTopTracks(token) {
    const response = await fetch("https://api.spotify.com/v1/me/top/tracks?limit=50", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!response.ok) throw new Error("Failed to fetch top tracks");
    return await response.json();
  }

  async function getSimilarTracks(token, seedTrackId) {
    const response = await fetch(`https://api.spotify.com/v1/recommendations?seed_tracks=${seedTrackId}&limit=10`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!response.ok) throw new Error("Failed to fetch similar tracks");
    return await response.json();
  }

  function downloadCSVFromTracks(data, filename) {
    const headers = ["id", "name", "artist", "album", "popularity", "duration_ms"];
    const rows = data.map(track => [
      track.id,
      `"${track.name.replace(/"/g, '""')}"`,
      `"${track.artists.map(a => a.name).join(", ").replace(/"/g, '""')}"`,
      `"${track.album.name.replace(/"/g, '""')}"`,
      track.popularity,
      track.duration_ms
    ]);

    const csvContent = [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    triggerDownload(blob, filename);
  }

  function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  window.onload = async () => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");

    if (code) {
      document.getElementById("message").innerText = "⏳ Fetching your top tracks and similar songs...";
      try {
        const tokenResponse = await getAccessToken(code);

        if (tokenResponse.access_token) {
          const topTrackData = await getTopTracks(tokenResponse.access_token);
          const topTracks = topTrackData.items;
          downloadCSVFromTracks(topTracks, "top_tracks.csv");

          // Pick the first track to get recommendations
          if (topTracks.length > 0) {
            const similarData = await getSimilarTracks(tokenResponse.access_token, topTracks[0].id);
            downloadCSVFromTracks(similarData.tracks, "similar_tracks.csv");
          }

          document.getElementById("message").innerText = "✅ Files downloaded: Top 50 Tracks & 10 Similar Songs!";
        } else {
          document.getElementById("message").innerText = "❌ Authorization failed.";
        }
      } catch (err) {
        document.getElementById("message").innerText = `❌ Error: ${err.message}`;
        console.error(err);
      }
    }
  };
  