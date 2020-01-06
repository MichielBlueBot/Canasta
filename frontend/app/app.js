import React from 'react';
import ReactDOM from 'react-dom';
import Game from './components/game/Game';
import styles from './app.module.scss';
import axios from 'axios';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            state: null,
            gameId: null,
            runningGames: [],
        };

        this.looping = false;
        this.playLoopTimeout = null;

        // Bind functions so they can access 'this'
        this.getGameIds = this.getGameIds.bind(this);
        this.selectGame = this.selectGame.bind(this);
        this.newGame = this.newGame.bind(this);
        this.playStep = this.playStep.bind(this);
        this.updateState = this.updateState.bind(this);
        this.playLoop = this.playLoop.bind(this);
        this.stopLoop = this.stopLoop.bind(this);
        this.quitGame = this.quitGame.bind(this);
    }

    componentDidMount() {
        // When we want to display this component, request our state from the backend
        this.getGameIds();
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

    getGameIds() {
        axios.get('http://localhost:4800/api/games')
             .then((res) => {
                this.setState({ runningGames: res.data });
              }, (error) => {
                console.log(error);
              });
    }

    selectGame(gameId) {
        this.setState({ gameId: gameId }, this.updateState);
    }

    newGame() {
        axios.get('http://localhost:4800/api/game')
             .then((res) => {
                this.setState({ gameId: res.data }, this.updateState);
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
            this.looping = true;
            axios.post('http://localhost:4800/api/game', { gameId: this.state.gameId })
              .then((res) => {
                this.updateState();
                if (!this.state.state.isFinished && this.looping) {  // Stop looping when game is finished
                    this.playLoopTimeout = setTimeout(this.playLoop, 100); // Call this function again after 50ms
                }
              }, (error) => {
                console.log(error);
              });
        }
    }

    stopLoop() {
        if (this.looping) {
            clearTimeout(this.playLoopTimeout);
            this.looping = false;
        }
    }

    quitGame() {
        this.setState({ state: null, gameId: null });
        this.getGameIds();
    }

    render() {
        const header = (
            <div className={styles.header}>
                <div className={styles.leftHeader}></div>
                <div className={styles.middleHeader}></div>
                <div className={styles.rightHeader}></div>
            </div>
        )
        if (this.state.state != null) {
          return (
                  <div>
                      {header}
                      <button onClick={this.newGame}>New game</button>
                      <button onClick={this.playStep}>Play step</button>
                      <button disabled={this.looping} onClick={this.playLoop}>Play loop</button>
                      <button disabled={!this.looping} className={styles.redButton} onClick={this.stopLoop}>Stop loop</button>
                      <button onClick={this.quitGame}>Quit game</button>
                      <br/>
                      <Game state={this.state.state}></Game>
                  </div>
                 )
        } else {
            const runningGameSelectors = [];
            for (const [index, gameId] of this.state.runningGames.entries()) {
                runningGameSelectors.push(<li key={index} className={styles.gameSelector} onClick={() => this.selectGame(gameId)}>Running game: {gameId}</li>)
            }
            return (
                <div>
                    {header}
                    <button onClick={this.newGame}>New game</button>
                    <ul>
                        {runningGameSelectors}
                    </ul>
                </div>
            )
        }
    }
};

ReactDOM.render(<App />, document.getElementById('app'));