import { ReactMediaRecorder } from "react-media-recorder";
import RecordIcon from "./RecordIcon";

type Props = {
  handleStop: any;
};
function RecordMessage({ handleStop }: Props) {
  return (
    <ReactMediaRecorder
      audio
      onStop={handleStop}
      render={({ status, startRecording, stopRecording }) => (
        <div className="mt-1">
          <button
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            className=" bg-purple-400 p-4 rounded-full shadow-sm"
          >
            <RecordIcon
              classText={
                status == "recording"
                  ? "animate-pulse text-red-500"
                  : "text-purple-800"
              }
            />
          </button>
          <p className="mt-1 text-purple-800 font-light uppercase font-sans">{status}</p>
        </div>
      )}
    />
  );
}
export default RecordMessage;
