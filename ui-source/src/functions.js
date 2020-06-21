import axios from 'axios';

export const getRequest = async(address, callback) => {
    let username = await localStorage.getItem('security-username');
    let password = await localStorage.getItem('security-password');
    if(!username || !password) {
        callback(false);
    }
    axios.get("/" + address + "?username=" + username + '&password=' + password).then((result) => {
        callback(true, result.data);
    }, (error) => {
        callback(false);
    });
}

export const deleteCredentials = async() => {
    await localStorage.removeItem('security-username');
    await localStorage.removeItem('security-password');
}

export const saveCredentials = async(username, password) => {
    await localStorage.setItem('security-username', username);
    await localStorage.setItem('security-password', password);
}

export const checkLoggedIn = async (callback) => {
    let username = await localStorage.getItem('security-username');
    let password = await localStorage.getItem('security-password');
    if(!username || !password) {
        callback(false);
    }
    
    apiLogin(username, password, callback);
}

export const apiLogin = (username, password, callback) => {
    axios.get("/login?username=" + username + '&password=' + password).then((result) => {
        console.log('resp', result.data);
        if(result.data == '1') {
            callback(true)
        } else {
            callback(false)
        }
    }, (error) => {
        callback(false);
    });
}