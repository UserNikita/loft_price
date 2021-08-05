import './App.css';
import {Container, CssBaseline, AppBar, Toolbar, Typography} from "@material-ui/core";
import ProxyTable from "./components/ProxyTable";

function App() {
    return (
        <div>
            <CssBaseline/>
            <AppBar position="fixed">
                <Toolbar>
                    <Typography variant="h6" noWrap>
                        Список прокси
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container>
                <Toolbar/>
                <ProxyTable/>
            </Container>
        </div>
    );
}

export default App;
