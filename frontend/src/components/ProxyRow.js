import {useState} from 'react';
import Button from '@material-ui/core/Button';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import CircularProgress from '@material-ui/core/CircularProgress';


export default function ProxyRow(props) {
    const apiHost = "http://localhost:5000"

    const [item, setItem] = useState(props.item);
    const [isLoaded, setIsLoaded] = useState(true);

    function refreshInfo(e) {
        console.log(item);
        setIsLoaded(false)

        fetch(apiHost + '/proxy/check?proxy=' + item.proxy)
            .then(res => res.json())
            .then(
                (result) => {
                    setIsLoaded(true);
                    setItem(result);
                }
            )

    }

    return (
        <TableRow>
            <TableCell>{item.id}</TableCell>
            <TableCell><code>{item.proxy}</code></TableCell>
            <TableCell>{item.country}</TableCell>
            <TableCell align="right">{item.elapsed}</TableCell>
            <TableCell>
                {isLoaded
                    ? <Button variant="contained" color="primary" onClick={refreshInfo}>Обновить</Button>
                    : <CircularProgress size={30}/>
                }
            </TableCell>
        </TableRow>
    )
}