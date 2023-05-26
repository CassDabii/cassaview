import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);


  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    const myMessage = { sender: "Me", blobUrl };
    const messageArr = [...messages, myMessage];

    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        await axios
          .post("http://127.0.0.1:8000/post-audio", formData, {
            headers: { "Content-Type": "audio/mpeg" },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobUrl(blob);

            const systemMessage = { sender: "Casper", blobUrl: audio.src };
            messageArr.push(systemMessage);
            setMessages(messageArr);
            console.log(messageArr)


            setIsLoading(false);
          })
          .catch((err) => {
            console.error(err.message);
            setIsLoading(false);
          });
      });
  };
  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        <div className=" mt-5 px-5">
          {messages.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  "flex flex-col " +
                  (audio.sender == "Casper" && "flex items-end")
                }
              >
                <div className=" mt-4">
                  <p
                    className={
                      audio.sender == "Casper"
                        ? "text-right mr-2 italic text-yellow-600"
                        : "ml-2 italic text-purple-800"
                    }
                  >
                    {audio.sender}
                  </p>
                  <audio
                    src={audio.blobUrl}
                    className="rounded-lg "
                    controls
                  />
                </div>
              </div>
            );
          })}

          {messages.length == 0 && !isLoading && (
            <div className="text-center font-light italic mt-6">Record your first message</div>
          )}

          {isLoading && (
            <div className="text-center font-light italic mt-6 animate-pulse">Compiling Response</div>
          )}

        </div>
        <div className="fixed bottom-0 w-full py-6 border-t text-center ">
          <div className="flex justify-center items-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
}
export default Controller;
