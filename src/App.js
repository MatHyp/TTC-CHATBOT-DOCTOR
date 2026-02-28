


import Chat from './Chat';
import SideBar from './modules/SideBar/SideBar';
import { Routes, Route } from 'react-router-dom';
import style from './main.module.css';

function App() {
  return (
    <div className={style.MainDiv}>
      <SideBar className={style.SideBar} />
        <Routes>
          <Route path="/" element={<div className={style.Chat}><Chat /></div>} />
          <Route path="/API" element={<Chat />} />
          <Route path="/about" element={< Chat/>} />
        </Routes>
    </div>
  );
}

export default App;