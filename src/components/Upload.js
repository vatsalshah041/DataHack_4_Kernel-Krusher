import React from 'react'
import {Button} from '@nextui-org/react'
import axios from 'axios'
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
                formData.append("file[]",files[i])
            }
            console.log(formData);
            uploading()
        }

        function uploading(){
            const FormData = require('form-data');
            // const fs = require('fs');
            let data = new FormData();
            for(let i=0;i<files.length;i++){
              console.log(files[i]);
              data.append("file[]",files[i])
          }

            let config = {
              method: 'post',
              maxBodyLength: Infinity,
              url: 'http://127.0.0.1:5000/upload',
              headers: { 
                'Content-Type': 'multipart/form-data', 
                // ...data.getHeaders()
              },
              data : data
            };

            async function makeRequest() {
              try {
                const response = await axios.request(config);
                console.log((response.data));
              }
              catch (error) {
                console.log(error);
              }
            }

            makeRequest();

        }

  return (
    <div>
      <input type='file' multiple onChange={handlechange}/>
      <Button onClick={handleUplaod} color='primary'>Upload </Button>
    </div>
  )
}
