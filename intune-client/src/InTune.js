import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import {
  useState,
  useEffect,
} from "react";

import {
  Button,
  Layout,
  Menu,
} from 'antd';

import ItGen from "./ItGen/ItGen";
import ItHome from "./ItHome/ItHome";
import ItRec from "./ItRec/ItRec";
import {UserContextProvider} from "./contexts/UserContext";

const { Header, Content, } = Layout;

export default function InTune() {
  return (
    <Router>
      <UserContextProvider>
        <Layout>
          <Header className="header">
            <div className="logo" />
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
              <Menu.Item key="1">
                <Link to="/">Home</Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/generation">Music Generation</Link>
              </Menu.Item>
              <Menu.Item key="3">
                <Link to="/recommendation">Music Recommendations</Link>
              </Menu.Item>
              {/*<Menu.Item key="4">*/}
                {/*<Button onClick = {loginToSpotify}> Login </Button>*/}
              {/*</Menu.Item>*/}
            </Menu>
          </Header>
          <Content style={{ margin: '50px' }}>
            <Routes>
              <Route path="/generation" element={<ItGen/>} />
              <Route path="/recommendation" element={<ItRec/>} />
              <Route path="/" element={<ItHome/>} />
            </Routes>
          </Content>
        </Layout>
      </UserContextProvider>
    </Router>
  );
}
