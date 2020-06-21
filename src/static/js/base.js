const getCredentials = () => {
    let username = localStorage.getItem('security-username');
    let password = localStorage.getItem('security-password');
    if(!username || !password) {
        return {};
    }
    return {
        username: username,
        password: password
    };
}

const saveCredentials = async (username, password) => {
    await localStorage.setItem('security-username', username);
    await localStorage.setItem('security-password', password);
}

const getRequest = (url, parameters, onResponse, onError) => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            onResponse(this.responseText)
        } else if(this.readyState === 4) {
            onError(this.responseText);
        }
    };
    if(Object.keys(parameters).length > 0) {
        url += '?';
    }
    let first = true;
    let keys = Object.keys(parameters);
    for(let i=0; i<keys.length; ++i) {
        url = url + (first ? '' : '&') + keys[i] + '=' + parameters[keys[i]];
        first = false;
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}