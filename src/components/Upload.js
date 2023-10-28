import React from 'react'
import {Button} from '@nextui-org/react'

import {useState} from 'react'
export default function Upload() {
        const [files,setFiles]=React.useState([])
        const handlechange=(e)=>{
            const files=e.target.files
            console.log(files)
            setFiles(files)
        }

        function handleUplaod(){
            const formData=new FormData()
            for(let i=0;i<files.length;i++){
                formData.append(`file${i}`,files[i])
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
