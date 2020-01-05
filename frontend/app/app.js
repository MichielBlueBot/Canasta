import React from 'react';
import ReactDOM from 'react-dom';
import Game from './components/game/Game';
import axios from 'axios';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            state: null,
            gameId: null,
        };

        this.playLoopTimeout = null;

        // Bind functions so they can access 'this'
        this.newGame = this.newGame.bind(this);
        this.playStep = this.playStep.bind(this);
        this.updateState = this.updateState.bind(this);
        this.playLoop = this.playLoop.bind(this);
        this.stopLoop = this.stopLoop.bind(this);
    }

    componentDidMount() {
        // When we want to display this component, request our state from the backend
        this.updateState();
    }

    updateState() {
        if (this.state.gameId != null) {
            const encodedGameId = encodeURIComponent(this.state.gameId);
            axios.get(`http://localhost:4800/api/state?gameId=${encodedGameId}`)
                 .then((res) => {
                     this.setState({ state: JSON.parse(res.data)});
                 }, (error) => {
                     console.log(error);
                 });
        }
    }

    newGame() {
        axios.get('http://localhost:4800/api/game')
             .then((res) => {
                this.setState({ gameId: res.data });
                this.updateState();
              }, (error) => {
                console.log(error);
              });
    }

    playStep() {
        if (this.state.gameId != null) {
            axios.post('http://localhost:4800/api/game', { gameId: this.state.gameId })
              .then((res) => {
                this.updateState();
              }, (error) => {
                console.log(error);
              });
        }
    }

    playLoop() {
        if (this.state.gameId != null) {
            axios.post('http://localhost:4800/api/game', { gameId: this.state.gameId })
              .then((res) => {
                this.updateState();
                if (!this.state.state.isFinished) {  // Stop looping when game is finished
                    this.playLoopTimeout = setTimeout(this.playLoop, 100); // Call this function again after 50ms
                }
              }, (error) => {
                console.log(error);
              });
        }
    }

    stopLoop() {
        if (this.playLoopTimeout != null) {
            clearTimeout(this.playLoopTimeout);
        }
    }

    render() {
          return (
                  <div>
                    <button onClick={this.newGame}>New game</button>
                    <button onClick={this.playStep}>Play step</button>
                    <button onClick={this.playLoop}>Play loop</button>
                    <button onClick={this.stopLoop}>Stop loop</button>
                    <br/>
                    <Game state={this.state.state}></Game>
                  </div>
                 )
        }
};

ReactDOM.render(<App />, document.getElementById('app'));