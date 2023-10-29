
import { Grid,Paper,Box } from '@mui/material'
import { ScrollShadow, Textarea } from '@nextui-org/react'
import * as React from 'react';
import {RadioGroup, Radio} from "@nextui-org/react";
import Upload from './Upload';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Slider from '@mui/material/Slider';
import { Button } from '@nextui-org/react';
import axios from 'axios';
export default function Home() {
  const [selected, setSelected] = React.useState("English");
  const [que,setQue]=React.useState("")
  const [ans,setAns]=React.useState("")
  const [trans,setTrans]=React.useState("")
  const marks = [
    {
      value: 0,
      label: '0',
    },
    {
      value: 20,
      label: '20',
    },
    {
      value: 40,
      label: '40',
    },
    {
      value: 60,
      label: '60',
    },{
      value: 80,
      label: '80',
    },
    {
      value: 100,
      label: '100+',
    },
  ];
  function valuetext(value) {
    return `${value}°C`;
  }
  
  function valueLabelFormat(value) {
    return marks.findIndex((mark) => mark.value === value) + 1;
  }
let t=''
  const translateque=(t)=>{
    let data = JSON.stringify({
        "text_to_translate": t,
      });

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:8000/translate',
        headers: { 
          'Content-Type': 'application/json'
        },
        data : data
      };

      async function makeRequest() {
        try {
          const response = await axios.request(config);
          console.log((response.data));
          setAns(response.data);
        }
        catch (error) {
          console.log(error);
        }
      }

      makeRequest();
  }

  const returnque=()=>{
    // console.log("t:",t);
const FormData = require('form-data');
let data1 = new FormData();
data1.append('query', que);

let config1 = {
  method: 'post',
  maxBodyLength: Infinity,
  url: 'http://127.0.0.1:5000/result',
  // headers: { 
  //   ...data1.getHeaders()
  // },
  data : data1
};

async function makeRequest1() {
  try {
    const response = await axios.request(config1);
    console.log("t:",response.data)
    t=response.data.response;
    translateque(t);
    // return response.data;
  }
  catch (error) {
    console.log(error);
  }
}
makeRequest1();

  }
  const filter=()=>{
    console.log(selected);
    returnque();
    // console.log(t);
    

  }

  return (
    <div style={{backgroundColor:""}}>
      <Grid container sx={{backgroundColor:""}}>
        <Grid item md={12} sx={{paddingTop:5,paddingLeft:50,justifyContent:"center",alignItems:"center"}}>
            <Upload/>
        </Grid>
        <Grid item md={6} sx={{padding:4}}>
        <Textarea
        maxRows={27}
        label="Your Translated pdf is here:"
        labelPlacement="outside"
        placeholder=""
        style={{height:"425px !important"}}
        className='textarea'
        // value={trans}
        // minRows={100}
      />
        </Grid>
        <Grid item md={6} sx={{padding:4}}>
          <Grid container>
            <Grid item md={12}>
            <Textarea
        maxRows={2}
        label="Question"
        labelPlacement="outside"
        placeholder="Enter your Question here"
        value={que}
        onChange={(e)=>{setQue(e.target.value);console.log(que);}}
        style={{}}
      />
            </Grid>
            <Grid item md={12} sx={{paddingTop:"5px",margindTop:5}}>
            <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Filter </Typography>
        </AccordionSummary>
        <AccordionDetails>
        <Box sx={{border:"2px solid black",borderRadius:"4px",padding:2}}>
              <RadioGroup
                  label="Select the language you want the answer in"
                  orientation="horizontal"
                  value={selected}
                  onChange={(e) => setSelected(e.target.value)}
              >
                <Radio value="English">English</Radio>
                <Radio value="Spanish">Spanish</Radio>
                <Radio value="French">French</Radio>
              </RadioGroup>
              
              <Box sx={{ width: 500 ,padding:2}}>
                Word Limit
                <Slider
                  aria-label="Always visible"
                  defaultValue={80}
                  getAriaValueText={valuetext}
                  step={10}
                  marks={marks}
                  valueLabelDisplay="on"
                />
              </Box>
                </Box>
        </AccordionDetails>
      </Accordion>
              
            </Grid>
            <Grid item md={12} sx={{paddingTop:"5px",margindTop:10,display: "flex", justifyContent: "flex-end", alignItems: "center"}}>
              <Button onClick={filter} color="primary">Submit</Button>
            </Grid>
          </Grid>
          <Grid item md={12}>
          <Textarea
        // maxRows={30}
        label="The answer to your query is this:"
        labelPlacement="outside"
        placeholder=""
        style={{}}
        value={ans?(selected==="English"?ans.original_text:selected==="Spanish"?ans.spanish_translation:selected==="French"?ans.french_translation:ans.original_text):""}
        minRows={100}/>
          </Grid>
        

        </Grid>
      </Grid>
    </div>
  )
}
