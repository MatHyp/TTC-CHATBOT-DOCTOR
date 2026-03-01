

import style from "./Text-Input.module.css";
import { useState } from "react";
function TextInput(props) {
	
  const [searchText, setSearchText] = useState("");
	
	
  const handleChangeSearch = (e) => {
		setSearchText(e.target.value);
  };
	
	
	
	
  return (
		<div>
			<form>
					
        <input className={style.textInput}
        
          type="text"
          placeholder="Search"
          onChange={handleChangeSearch}
          value={searchText}
        />
		<button onClick={props.SendPrompt}className={style.SendPrompt}><i class="icon-paper-plane"></i></button>
			
			</form>
		
		</div>
		
  );
}

export default TextInput;
