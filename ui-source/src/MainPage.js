import React from 'react';
import PropTypes from 'prop-types';
import {checkLoggedIn, saveCredentials, getRequest, deleteCredentials, apiLogin} from './functions';

class MainPage extends React.Component {
    
    interval = null;
    
    static propTypes = {
    
    }
    
    state = {
        loggedIn: false,
        
        username: '',
        password: '',
        
        active: false,
        movementFactor: 0,
        movementActive: false,
        
        info: '',
        feed: '',
        altered: '',
    }
    
    componentDidMount() {
        this.update();
        setTimeout(() => {
            /*saveCredentials('admin', 'admin').then(() => {
                this.update();
            })*/
        }, 2000);
    }
    
    update = () => {
        checkLoggedIn((isLoggedIn) => {
            this.setState({
                loggedIn: isLoggedIn,
            });
            
            if(isLoggedIn) {
                this.interval = setInterval(() => {
                    this.getMovementFactor();
                    this.getFeed();
                    this.getActive();
                    this.getAltered();
                    this.getInfo();
                }, 1000);
            }
        })
    }
    
    render() {
        
        if(this.state.loggedIn) {
            return (
                <div style={{
                    width: '100%',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <div style={{width: '60%', minWidth: 400, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'flex-start'}}>
                        <div style={{fontWeight: 'bold', width: '100%', marginBottom: 4, textAlign: 'left', color: '#666', fontSize: 14, paddingLeft: 20, paddingRight: 20}}>
                            {
                                "Statusul alarmei"
                            }
                        </div>
                        <div style={{borderRadius: 2, width: '100%', marginBottom: 4, textAlign: 'left', backgroundColor: '#eee', color: '#333', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                this.state.active ? 'Alarma activa' : 'Alarma dezactivata'
                            }
                        </div>
                        <div onClick={this.onToggleActive} style={{borderRadius: 2, cursor: 'pointer', transitionDuration: 1.0, width: '100%', marginBottom: 8, textAlign: 'left', backgroundColor: this.state.active ? '#450606' : '#283b06', color: '#fff', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                this.state.active ? 'Dezactiveaza alarma' : 'Activeaza alarma'
                            }
                        </div>
    
                        <div style={{fontWeight: 'bold', width: '100%', marginBottom: 4, textAlign: 'left', color: '#666', fontSize: 14, paddingLeft: 20, paddingRight: 20}}>
                            {
                                "Informatii placuta"
                            }
                        </div>
                        <div style={{borderRadius: 2, width: '100%', marginBottom: 8, textAlign: 'left', backgroundColor: '#eee', color: '#333', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                this.state.info
                            }
                        </div>
    
                        <div style={{fontWeight: 'bold', width: '100%', marginBottom: 4, textAlign: 'left', color: '#666', fontSize: 14, paddingLeft: 20, paddingRight: 20}}>
                            {
                                "Factorul de miscare"
                            }
                        </div>
                        <div style={{borderRadius: 2, width: '100%', marginBottom: 8, textAlign: 'left', backgroundColor: '#eee', color: '#333', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                this.state.movementFactor
                            }
                        </div>
    
                        <div style={{fontWeight: 'bold', width: '100%', marginBottom: 4, textAlign: 'left', color: '#666', fontSize: 14, paddingLeft: 20, paddingRight: 20}}>
                            {
                                "Statusul miscarii"
                            }
                        </div>
                        <div style={{borderRadius: 2, width: '100%', marginBottom: 8, textAlign: 'left', backgroundColor: '#eee', color: '#333', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                this.state.movementActive ? "Miscare detectata!" : 'Nicio miscare detectata!'
                            }
                        </div>
                        
                        <div style={{width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8}}>
                            <img src={'data:image/png;base64,' + this.state.feed} style={{width: '49%', borderRadius: 2,}}/>
                            <img src={'data:image/png;base64,' + this.state.altered} style={{width: '49%', borderRadius: 2,}}/>
                        </div>
    
                        <div onClick={this.onLogout} style={{borderRadius: 2, cursor: 'pointer', transitionDuration: 1.0, width: '100%', marginBottom: 8, textAlign: 'left', backgroundColor: '#450606', color: '#fff', fontSize: 18, paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20}}>
                            {
                                'Deautentificare'
                            }
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div style={{width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', fontSize: 18}}>
                    <div style={{width: '30%', textAlign: 'left', paddingBottom: 4, color: '#333'}}>
                        {"Utilizator"}
                    </div>
                    <input placeholder={'Introduceti utilizatorul'} style={{color: '#333', padding: 20, fontSize: 18, marginBottom: 8, backgroundColor: '#eee', outlineColor: 'transparent', borderRadius: 2, borderColor: 'transparent', paddingTop: 10, paddingBottom: 10, minWidth: '30%'}} type={'text'} onChange={this.onUsernameChange}/>
                    <div style={{width: '30%', textAlign: 'left', paddingBottom: 4, color: '#333'}}>
                        {"Parola"}
                    </div>
                    <input placeholder={'Introduceti parola'} style={{color: '#333', padding: 20, fontSize: 18, marginBottom: 8, backgroundColor: '#eee', outlineColor: 'transparent', borderRadius: 2, borderColor: 'transparent', paddingTop: 10, paddingBottom: 10, minWidth: '30%'}} type={'password'} onChange={this.onPasswordChange}/>
                    <div onClick={this.onLogin} style={{backgroundColor: '#eee', paddingTop: 10, paddingBottom: 10, paddingLeft: 20, paddingRight: 20, cursor: 'pointer', fontSize: 18, minWidth: '30%',}}>
                        {
                            'Autentificare'
                        }
                    </div>
                </div>
            );
        }
        
    }
    
    onUsernameChange = (event) => {
        this.setState({
            username: event.target.value,
        });
    }
    
    onPasswordChange = (event) => {
        this.setState({
            password: event.target.value,
        });
    }
    
    onLogin = () => {
        apiLogin(this.state.username, this.state.password, (successful) => {
            if(successful) {
                saveCredentials(this.state.username, this.state.password).then(() => {
                    this.update();
                })
            }
        })
    }
    
    onLogout = () => {
        deleteCredentials().then(() => {
            this.update();
        });
    }
    
    
    onToggleActive = () => {
        getRequest('toggle-active', (successful, response) => {
        
        });
    }
    
    getInfo = () => {
        getRequest('get-info', (successful, response) => {
            if(successful) {
                this.setState({
                    info: response
                })
            }
        })
    }
    
    getMovementFactor = () => {
        getRequest('movement', (successful, response) => {
            if(successful) {
                this.setState({
                    movementFactor: response.factor,
                    movementActive: response.active == '1',
                });
            }
        });
    }
    
    getActive = () => {
        getRequest('get-active', (successful, response) => {
            if(successful) {
                this.setState({
                    active: response == '1'
                })
            }
        })
    }
    
    getFeed = () => {
        getRequest('feed', (successful, response) => {
            if(successful) {
                this.setState({
                    feed: response,
                });
            }
        });
    }
    
    getAltered = () => {
        getRequest('altered', (successful, response) => {
            if(successful) {
                this.setState({
                    altered: response,
                });
            }
        });
    }
}

export default MainPage;