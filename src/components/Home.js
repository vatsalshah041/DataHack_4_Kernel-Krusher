
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

export default function Home() {
  const [selected, setSelected] = React.useState("English");
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
  return (
    <div style={{backgroundColor:""}}>
      <Grid container sx={{backgroundColor:""}}>
        <Grid item md={12} sx={{paddingTop:5,paddingLeft:50,justifyContent:"center",alignItems:"center"}}>
            <Upload/>
        </Grid>
        <Grid item md={6} sx={{padding:4}}>
        <Textarea
        // maxRows={30}
        label="Your Translated pdf is here:"
        labelPlacement="outside"
        placeholder=""
        style={{}}
        minRows={100}
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
          </Grid>
        

        </Grid>
      </Grid>
    </div>
  )
}
