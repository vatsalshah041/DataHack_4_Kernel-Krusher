// "use client";
// // import NextLink from "next/link";

// // Third-party imports
// const {
//   Navbar: NextUINavbar,
//   NavbarContent,
//   NavbarMenu,
//   NavbarMenuToggle,
//   NavbarBrand,
//   NavbarItem,
//   NavbarMenuItem,
// } = require("@nextui-org/navbar");
// const { Link } = require("@nextui-org/link");
// const { Tab, Tabs } = require("@nextui-org/tabs");
// const { button: buttonStyles } = require("@nextui-org/theme");
// const { Scale } = require("lucide-react");

// // Component imports
// const ColorModeSwitchButton = require("@/components/ColorModeSwitchButton");
// // const {
// //   navbarLinksForHome,
// //   NavLinksDisplayedOnHomePage,
// // } = require("@/components/NavLinks");
// // const useActiveSection = require("@/hooks/useActiveSection");
// const SearchButton = require("./SearchButton");

// module.exports.Navbar = () => {
//   const { activeSection, setActiveSection, setTimeOfLastClick } =
//     useActiveSection();

//   const handlingManualSectionChange = (activeSection) => {
//     setActiveSection(activeSection);
//     setTimeOfLastClick(Date.now());
//   };

//   return (
//     <NextUINavbar maxWidth="full" position="sticky" aria-selected>
//       <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
//         <NavbarBrand className="gap-3 max-w-fit">
//           {/* <NextLink className="flex justify-start items-center" href="/"> */}
//             <Scale className="mr-2" />
//             <p className="font-bold text-inherit text-lg">Aapka Adhikar</p>
//           {/* </NextLink> */}
//         </NavbarBrand>

//         <div className="hidden md:flex ml-10 mr-2">
//           <Tabs
//             aria-label="Options"
//             variant="underlined"
//             size="md"
//             color="primary"
//             classNames={{
//               tabList: "gap-[1]",
//             }}
//             selectedKey={activeSection}
//             onSelectionChange={(key) => handlingManualSectionChange(key)}
//           >
//             {navbarLinksForHome.map((navbarLink) => {
//               return (
//                 <Tab
//                   as={Link}
//                   key={navbarLink.title}
//                   title={navbarLink.title}
//                   href={navbarLink.href}
//                 />
//               );
//             })}
//           </Tabs>
//         </div>

//         <NavbarItem className="hidden lg:flex">
//           <SearchButton />
//         </NavbarItem>
//       </NavbarContent>

//       <NavbarContent
//         className="hidden sm:flex basis-1/5 sm:basis-full"
//         justify="end"
//       >
//         <NavbarItem className="hidden sm:flex gap-2">
//           <ColorModeSwitchButton />
//         </NavbarItem>
//         <NavbarItem>
//           <Link href="/login" className={buttonStyles({ variant: "faded" })}>
//             Login
//           </Link>
//         </NavbarItem>
//       </NavbarContent>

//       <NavbarContent className="sm:hidden basis-1 pl-4" justify="end">
//         <NavbarItem>
//           <NavbarMenuToggle />
//         </NavbarItem>
//         <NavbarItem>
//           <Link href="/login" className={buttonStyles({ variant: "faded" })}>
//             Login
//           </Link>
//         </NavbarItem>
//       </NavbarContent>

//       <NavbarMenu>
//         <NavbarItem>
//           <ColorModeSwitchButton />
//         </NavbarItem>
//         <div className="mx-4 mt-2 flex flex-col gap-2">
//           {navbarLinksForHome.map((navbarLink, index) => (
//             <NavbarMenuItem key={`${index}`}>
//               <Link
//                 color={
//                   navbarLink.title === activeSection ? "primary" : "foreground"
//                 }
//                 href={navbarLink.href}
//                 size="lg"
//               >
//                 {navbarLink.title}
//               </Link>
//             </NavbarMenuItem>
//           ))}
//         </div>
//       </NavbarMenu>
//     </NextUINavbar>
//   );
// };
