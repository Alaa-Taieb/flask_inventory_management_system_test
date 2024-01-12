const HOST = sessionStorage.getItem('host');
const GET_HOST_URL = "/utils/host";
if (!HOST){
    fetch(GET_HOST_URL)
    .then(res => res.json())
    .then(data => {
        sessionStorage.setItem('host', data.host);
        console.log("HOST LOADED")
    })
}
