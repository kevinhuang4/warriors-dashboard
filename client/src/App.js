import './App.css';
import Standings from './components/Standings';
import Recent from './components/Recent';
import LastGame from './components/LastGame';
import Injuries from './components/Injuries';
import PlayerStats from './components/PlayerStats';

function App() {
  return (
    <div className="App">
      <Standings />
      <Recent />
      <LastGame />
      <Injuries />
      <PlayerStats />
    </div>
  );
}

export default App;
