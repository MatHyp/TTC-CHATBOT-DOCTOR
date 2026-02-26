import style from "./Burger.module.css";
import { useState } from "react";
function Burger({DoAfterClick}) {
	
	//const [ShowPanel, setShowPanel] = useState(false);

  return (
	<div className={style.Burger} onClick={DoAfterClick}>
		<div className={style.Burgerline}></div>
		<div className={style.Burgerline}></div>
		<div className={style.Burgerline}></div>
	</div>
  );
}

export default Burger;
