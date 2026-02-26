import style from "./SideBar.module.css";
import Burger from "../Burger-icon/Burger.js";
import { useState } from "react";
function SideBar({className}) {
	
	const [ShowPanel, setShowPanel] = useState(false);
const changeState = () => {
  setShowPanel(prev => !prev);
};
  return (
	<>
		<Burger DoAfterClick={changeState}/>
		<div className={`${className} ${ShowPanel  ? style.sideBarLocal : style.sideBarLocalDezactive }`} >

		</div>
  </>);
}

export default SideBar;
