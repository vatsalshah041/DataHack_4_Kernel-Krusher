import React from 'react'
import {Button} from '@nextui-org/react'

import {useState} from 'react'
export default function Upload() {
        const [files,setFiles]=React.useState([])
        const handlechange=(e)=>{
            const newfiles=e.target.files
            console.log('hi');
            console.log(files)
            setFiles([...files, ...newfiles]);
        }

        function handleUplaod(){
            const formData=new FormData()
            for(let i=0;i<files.length;i++){
                console.log(files[i]);
                formData.append("file",files[i])
            }
            console.log(formData);
            
        }

  return (
    <div>
      <input type='file' multiple onChange={handlechange}/>
      <Button onClick={handleUplaod} color='primary'>Upload </Button>
    </div>
  )
}
