import style from "./Messages.module.css";

export  function Sender(props) {
	
	
	
	
	
  return (

		<div className={`${style.Smes} ${style.mes}`}>
			<p>{props.Text}</p>
		</div>
  );
}
export  function Reciver(props) {
	
	
	
	
	
  return (

		<div className={`${style.Rmes} ${style.mes}`}>
			<p>{props.Text}</p>
		</div>
  );
}
