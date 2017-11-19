import React from 'react';
import { configure, shallow } from 'enzyme';
import ExampleWork, {ExampleWorkBubble} from '../js/example-work';
import Adapter from 'enzyme-adapter-react-15';
configure({ adapter: new Adapter() });
const myWork = [
  {
    'title':"Something Stupid",
    'image':{
      'desc':"example screenshot of a project involving code",
      'src':"images/example1.png",
      'comment':""
    }
  },
  {
    'title':"Tripatra",
    'image':{
      'desc':"example screenshot of a project involving chemistry",
      'src':"images/example2.png",
      'comment':`/*-- “Chemistry” by Surian Soosay is licensed under CC BY 2.0
           https://www.flickr.com/photos/ssoosay/4097410999 -->*/`
    }
  }
];


describe("ExampleWork component", () => {
let component = shallow(<ExampleWork work={myWork}/>);
it("Should be a 'span' element", () => {
    expect(component.type()).toEqual('section');
});
it("should contain as many children as there are work examples",()=>{
  expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
});
});
describe("ExampleWorkBubble component", ()=>{
  let component = shallow(<ExampleWorkBubble example={myWork[1]}/>);
  let images = component.find("img");
  it("should contain a single 'img' element", ()=>{
    expect(images.length).toEqual(1);
  });
  it("should have the img src set correctly", () =>{
    expect(images.getElement().props.src).toEqual(myWork[1].image.src);
  });
});
