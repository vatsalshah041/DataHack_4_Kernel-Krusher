import React from "react";
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button} from "@nextui-org/react";
import { AcmeLogo } from "./Acmelogo";

export default function Navbars() {
  return (
    <div style={{backgroundColor:"black"}}>
    <Navbar>
      <NavbarBrand >
        <AcmeLogo />
        <p className="font-bold text-inherit"></p>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-30" justify="center">
        
       
      </NavbarContent>
      <NavbarContent justify="end">
     
        <NavbarItem>
          <Button as={Link} color="primary" variant="flat">
            LAWYANTRA
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
    </div>
  );
}
