import Alert from "@mui/material/Alert"
import Button from "@mui/material/Button"
import Stack from "@mui/material/Stack"
import TextField from "@mui/material/TextField"
import Typography from "@mui/material/Typography"
import React, { useEffect, useState } from 'react'
import { fetchCaptcha, fetchComments, postComment } from "./Controllers"
import { CaptchaResponse, Comment, Location } from "./Types"


const CAPTCHA_ALPHABET = new Set([
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
])
const CAPTCHA_TEXT_LENGTH = 6


export default function Comments({location}: {location: Location}) {
    const [previousComments, setPreviousComments] = useState<JSX.Element[]>([])
    const [previousCommentsErrorEl, setPreviousCommentsErrorEl] = useState<React.ReactNode>("")

    const [newCommentAuthorName, setNewCommentAuthorName] = useState<string>("")
    const [newCommentContent, setNewCommentContent] = useState<string>("")
    const [captcha, setCaptcha] = useState<CaptchaResponse | null>(null)
    const [captchaAnswer, setCaptchaAnswer] = useState<string>("")
    const [captchaAnswerHasError, setCaptchaAnswerHasError] = useState<boolean>(false)
    const [captchaHelpMsg, setCaptchaHelpMsg] = useState<string>(
        "Tragen Sie die oben angegeben Zeichen hier ein"
    )
    const [newCommentAuthorNameErrorText, setNewCommentAuthorNameErrorText] = useState<string>("")
    const [newCommentContentErrorText, setNewCommentContentErrorText] = useState<string>("")
    const [newCommentPostErrorEl, setNewCommentPostErrorEl] = useState<React.ReactNode>("")

    const handleOnChangeNewCommentAuthorName = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNewCommentAuthorName(e.target.value)

        if (e.target.value !== "") {
            setNewCommentAuthorNameErrorText("")
        }
    }

    const handleOnChangeNewCommentContent = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNewCommentContent(e.target.value)

        if (e.target.value !== "") {
            setNewCommentContentErrorText("")
        }
    }

    const handleOnChangeCaptchaAnswer = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        if (e.target.value.length > CAPTCHA_TEXT_LENGTH) {
            setCaptchaHelpMsg("Der Text sollte 6 Zeichen lang sein")
            return
        }

        const validChars = []

        for (const char of e.target.value) {
            const capitalChar = char.toUpperCase()
            if (CAPTCHA_ALPHABET.has(capitalChar)) {
                validChars.push(capitalChar)
            } else {
                setCaptchaHelpMsg("Verwenden Sie nur Zahlen 0-9 oder Buchstaben A-Z")
            }
        }

        const answer = validChars.join("")
        
        if (answer !== "") {
            setCaptchaAnswerHasError(false)
        }

        setCaptchaAnswer(answer)
    }

    const handleSubmitNewComment = (e: React.FormEvent): void => {
        e.preventDefault()

        let hasUnfilledContent = false

        if (newCommentAuthorName === "") {
            setNewCommentAuthorNameErrorText("Bitte geben Sie einen Namen an!")
            hasUnfilledContent = true
        }

        if (newCommentContent === "") {
            setNewCommentContentErrorText("Bitte fügen Sie den Kommentar Inhalt hinzu!")
            hasUnfilledContent = true
        }

        if (captchaAnswer === "") {
            setCaptchaAnswerHasError(true)
            setCaptchaHelpMsg("Bitte tragen Sie den oben angegeben Zeichen ein!")
            hasUnfilledContent = true
        }

        if (hasUnfilledContent) {
            return
        }

        postComment({
            captcha_token: captcha?.token as string,
            captcha_answer: captchaAnswer,
            location_id: location.id,
            author_name: newCommentAuthorName,
            content: newCommentContent,
        }).then(() => {
            // Reset content to blank
            setNewCommentContent("")
            setCaptcha(null)
            setCaptchaAnswer("")
            setCaptchaAnswerHasError(false)
            setCaptchaHelpMsg("Tragen Sie die oben angegeben Zeichen hier ein")
            
            updatePreviousComments()
            updateCaptcha()
        }).catch((err) => {
            const res = err.response;
            if (res) {
                if (res.status === 401) {
                    setCaptchaAnswerHasError(true)
                    setCaptchaHelpMsg(
                        "Ihre Antwort war falsch. Bitte tragen Sie den oben angegeben Zeichen neu ein!"
                    )

                    setCaptcha({
                        token: res.data.detail.new_captcha_token as string,
                        jpeg: res.data.detail.new_captcha_jpeg as string,
                    })
                    setCaptchaAnswer("")
                    return
                }

                if (res.status === 413) {
                    switch (res.data.detail.field) {
                        case "captcha_answer":
                            setCaptchaAnswerHasError(true)
                            setCaptchaHelpMsg("Der Text sollte 6 Zeichen lang sein!")
                            return
                        case "author_name":
                            setNewCommentAuthorNameErrorText(
                                `Der Authornamen darf maximal ${res.data.detail.max_len} Zeichen lang sein!`
                            )
                            return
                        case "content":
                            setNewCommentContentErrorText(
                                `Der Kommentar dar maximal ${res.data.detail.max_len} Zeichen lang sein!`
                            )
                            return
                    }
                }

                console.error(`Post new comment has unexpected response: ${JSON.stringify(res)}`)
            }
            console.error(`Failed to post new comment: ${err.message}`)

            setNewCommentPostErrorEl(<Alert severity="error" sx={{ mb: 2 }}>
                Der Kommentar könnte leider nicht gespeichert werden.<br />
                Bitte kontaktieren Sie unsere Entwicklerteam.
            </Alert>)
        })
    }

    const newCommentHasError = (): boolean => {
        return (
            newCommentAuthorNameErrorText !== "" 
            || newCommentContentErrorText !== "" 
            || newCommentPostErrorEl !== ""
        )
    }

    const updatePreviousComments = (): void => {
        fetchComments(location.id).then((comments: Comment[]): void => {
            const sortedCommentsNewestFirst = comments.sort(
                (a, b) => Date.parse(b.timestamp) - Date.parse(a.timestamp)
            )

            setPreviousComments(sortedCommentsNewestFirst.map((comment: Comment) => {
                let localDateTimeString;
                try {
                    localDateTimeString = (new Date(`${comment.timestamp}Z`)).toLocaleString()
                } catch (err) {
                    localDateTimeString = ""
                    console.error(`Failed to convert timestamp ${comment.timestamp} to german date string: ${err}`)
                }

                return(<div key={comment.id}>
                    <Typography variant="h6">
                        {comment.author_name}
                    </Typography>
                    {localDateTimeString && <Typography variant="caption">{localDateTimeString}</Typography>}
                    <Typography 
                        paragraph
                        sx={{ mb: 2 }}
                    >{comment.content}</Typography>
                </div>)
            }))
        }).catch((err) => {
            console.error(`Failed to fetch previous comments: ${err.message}`)

            setPreviousCommentsErrorEl(<Alert severity="error">
                Alte Kommentare könnten nicht abgerufen werden.<br />
                Bitte kontaktieren Sie unsere Entwicklerteam.
            </Alert>)
        })
    }

    const updateCaptcha = (): void => {
        fetchCaptcha().then((captcha) => {
            setCaptcha(captcha)
        })
    }

    useEffect(() => {
        updatePreviousComments()
        updateCaptcha()
    }, [])

    return(
        <>
            <form noValidate action="/comment" method="POST" onSubmit={handleSubmitNewComment}>
                <TextField 
                    id="author-name-input" 
                    name="author_name" 
                    label="Author" 
                    type="string"
                    value={newCommentAuthorName}
                    onChange={handleOnChangeNewCommentAuthorName}
                    error={newCommentHasError()}
                    helperText={newCommentAuthorNameErrorText}
                    autoComplete='off'
                    fullWidth
                    disabled={captcha === null}
                    required
                    sx={{ mt: 1, mb: 2 }}
                />
                <TextField 
                    id="content-input" 
                    name="content" 
                    label="Kommentar" 
                    type="string"
                    value={newCommentContent}
                    onChange={handleOnChangeNewCommentContent}
                    error={newCommentHasError()}
                    helperText={newCommentContentErrorText}
                    autoComplete='off'
                    fullWidth
                    multiline
                    rows={4}
                    disabled={captcha === null}
                    required
                    sx={{ mb: 2 }}
                />
                {captcha && <>
                    <img src={`data:image/jpeg;base64,${captcha?.jpeg}`} />
                    <TextField 
                        id="captcha-input" 
                        name="content" 
                        label="Captcha" 
                        type="string"
                        value={captchaAnswer}
                        onChange={handleOnChangeCaptchaAnswer}
                        error={captchaAnswerHasError}
                        helperText={captchaHelpMsg}
                        autoComplete='off'
                        fullWidth
                        multiline
                        required
                        sx={{ mt: 2, mb: 2 }}
                    />
                </>}
                {newCommentPostErrorEl}
                <Button 
                    variant="contained" 
                    type="submit"
                    color="primary" 
                    disabled={captcha === null}
                    sx={{ mb: 2 }}
                >
                    Kommentar hinterlassen
                </Button>
            </form>

            {previousCommentsErrorEl}
            {previousComments.length !== 0 && <>
                <Stack>
                    {previousComments}
                </Stack>
            </>}
        </>
    )
}